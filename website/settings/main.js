let ip = localStorage.getItem("ip")
let port = localStorage.getItem("port")
if (!port) {
	port = "2754"
}
if (!ip) {
	ip = window.location.host + ":" + port
} else {
	ip = ip + ":" + port
}

function httpGet(url) {
	let xmlHttpReq = new XMLHttpRequest()
	xmlHttpReq.open("GET", url, false)
	xmlHttpReq.send(null)
	return xmlHttpReq.responseText
}

window.onload = () => {
	document.getElementById("ip").value = ip
	document.getElementById("port").value = port
	let presets = httpGet("http://" + ip + "/getPresets")
	let presetl = presets.split("\n")
	presetl.pop()
	let presetsel = document.getElementById("preset")
	presetl.forEach((preset) => {
		let option = document.createElement("option")
		option.id = preset
		option.innerHTML = preset
		presetsel.appendChild(option)
	})
}

function save() {
	preset = document.getElementById("preset").value
	ip = document.getElementById("ip").value
	port = document.getElementById("port").value
	localStorage.setItem("preset", preset)
	localStorage.setItem("ip", ip)
	localStorage.setItem("port", port)
	document.location.pathname = document.location.pathname.replace("/settings/", "")
}