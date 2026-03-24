// 获取客户端公网IP
export async function getClientIP() {
    try {
        const res = await fetch('https://api.ipify.org?format=json');
        const data = await res.json();
        return data.ip;
    } catch (err) {
        return 'unknown';
    }
}