const API_ROBOT = '/dashboard/api/robot-position/latest/';
const API_TRAFFIC = '/dashboard/api/traffic/';

const canvas = document.getElementById('robotMap');
const ctx = canvas.getContext('2d');
const width = canvas.width;
const height = canvas.height;

function drawMap(x, y) {
    // Clear
    ctx.clearRect(0, 0, width, height);
    
    // Draw Grid (Background is CSS)
    
    // Draw Robot
    // Map logic: 0,0 is center? Or top left? Let's assume 0-100 range mapped to canvas.
    // If coords are meters, let's assume 50x50m area.
    const scale = width / 100; 
    const drawX = (x || 50) * scale; // Default center
    const drawY = (y || 50) * scale;

    ctx.beginPath();
    ctx.arc(drawX, drawY, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#0f0';
    ctx.fill();
    
    // Pulse effect
    ctx.beginPath();
    ctx.arc(drawX, drawY, 15, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.5)';
    ctx.stroke();
}

async function updateRobot() {
    try {
        const res = await fetch(API_ROBOT);
        const data = await res.json();
        
        if (data.x !== undefined) {
            document.getElementById('val-x').innerText = data.x.toFixed(2);
            document.getElementById('val-y').innerText = data.y.toFixed(2);
            
            // Render Env Data
            const envDiv = document.getElementById('env-data');
            envDiv.innerHTML = '';
            if (data.atmosphere) {
                for (const [key, val] of Object.entries(data.atmosphere)) {
                    envDiv.innerHTML += `<div class="metric-box"><span class="label">${key}:</span> <span class="value">${val}</span></div>`;
                }
            }
            
            drawMap(data.x, data.y);
        }
    } catch (e) {
        console.error("Robot Fetch Error", e);
    }
}

async function updateTraffic() {
    try {
        const res = await fetch(API_TRAFFIC);
        const data = await res.json();
        
        const tbody = document.querySelector('#traffic-table tbody');
        tbody.innerHTML = ''; // Clear
        
        if (data.flows) {
            data.flows.forEach(flow => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${flow.src_ip || 'N/A'}</td>
                    <td>${flow.dst_ip || 'N/A'}</td>
                    <td>${flow.protocol || 'N/A'}</td>
                    <td>${flow.length || flow.packet_length || 'N/A'}</td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (e) {
        console.error("Traffic Fetch Error", e);
    }
}

// Init
drawMap(50, 50);
setInterval(updateRobot, 1000);
setInterval(updateTraffic, 5000);
updateTraffic();
