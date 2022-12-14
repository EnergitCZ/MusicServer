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
let songlist = []
let preset = localStorage.getItem("preset")
if (!preset) {
	preset = "128_opus"
}
let audioplayer1 = new Audio()
let audioplayer2 = new Audio()
let cap = 1
let setup = false
let progressbar

window.onload = () => {
	updateSongs(40)
	updateSongList()
	progressbar = document.getElementById("progressbar")
}

function getCurrentAudioPlayer() {
	if (cap == 1) {
		return audioplayer1
	} else {
		return audioplayer2
	}
}

function getOtherAudioPlayer() {
	if (cap == 1) {
		return audioplayer2
	} else {
		return audioplayer1
	}
}

function changeAudioPlayer() {
	if (cap == 1) {
		cap = 2
	} else {
		cap = 1
	}
}

function checkFF() {
	let ua = navigator.userAgent
	if (ua.match(/firefox|fxios/i)) {
		return true
	}
	return false
}

function httpGet(url) {
	let xmlHttpReq = new XMLHttpRequest()
	xmlHttpReq.open("GET", url, false)
	xmlHttpReq.send(null)
	return xmlHttpReq.responseText
}

function reverseArray(array) {
	let newArr = [];
	for(i = array.length-1; i >= 0; i--) {
		newArr.push(array[i])
	}
	return newArr;
}

function appendSongList(item) {
	if (item) {
		split = item.split("\n")
		split[1] = JSON.parse(split[1])
		songlist.unshift(split)
	}
}

function updateSongList() {
	let table = document.getElementById("songs")
	table.innerHTML = ""
	reverseArray(songlist).forEach((item)=>{
		let tr = document.createElement("tr")
		let td1 = document.createElement("td")
		let td2 = document.createElement("td")
		let td3 = document.createElement("td")
		td1.innerText = item[1]["artist"][0]
		td2.innerText = item[1]["title"][0]
		var h = Math.floor(item[1]["duration"] / 3600);
		if (h) {
			td3.innerText = h + ":"
		}
		var m = Math.floor(item[1]["duration"] % 3600 / 60);
		if (m) {
			if (m < 10) {
				td3.innerText = td3.innerText + "0" + m + ":"
			} else {
				td3.innerText = td3.innerText + m + ":"
			}
		} else {
			td3.innerText = td3.innerText + "00:"
		}
		var s = Math.floor(item[1]["duration"] % 3600 % 60);
		if (s < 10) {
			td3.innerText = td3.innerText + "0" + s
		} else {
			td3.innerText = td3.innerText + s
		}
		tr.appendChild(td1)
		tr.appendChild(td2)
		tr.appendChild(td3)
		table.appendChild(tr)
	})
}

function setSongActive(song) {
	let table = document.getElementById("songs")
	table.firstChild.style.background = "green"
	table.firstChild.children[0].style.color = "FFF"
	table.firstChild.children[1].style.color = "FFF"
	progressbar.max = song[1]["duration"]
	document.title = song[1]["artist"][0] + " - " + song[1]["title"][0]
}

function updateSongs(amount) {
	let unparsed = httpGet("http://"+ip+"/getRandomFiles/" + amount.toString())
	let songs = unparsed.split("\n\n")
	//songlist = []
	songs.forEach(appendSongList)
}

let play

if (checkFF()) {
	play = function () {
		if (!setup) {
			updateSongList()
			song = songlist.pop()
			setSongActive(song)
			src = "http://"+ip+"/getEncFile/" + preset + "/" + encodeURIComponent(song[0].substring(1))
			getCurrentAudioPlayer().src = src
			getCurrentAudioPlayer().load()
			getCurrentAudioPlayer().play()
			src = "http://"+ip+"/getEncFile/" + preset + "/" + encodeURIComponent(songlist.at(-1)[0].substring(1))
			getOtherAudioPlayer().src = src
			getOtherAudioPlayer().load()
		} else {
			updateSongList()
			song = songlist.pop()
			setSongActive(song)
			changeAudioPlayer()
			getOtherAudioPlayer().pause()
			getCurrentAudioPlayer().play()
			src = "http://"+ip+"/getEncFile/" + preset + "/" + encodeURIComponent(songlist.at(-1)[0].substring(1))
			getOtherAudioPlayer().src = src
			getOtherAudioPlayer().load()
		}
		setup = true
	}
} else {
	play = function () {
		updateSongList()
		song = songlist.pop()
		setSongActive(song)
		src = "http://"+ip+"/getEncFile/" + preset + "/" + encodeURIComponent(song[0].substring(1))
		getCurrentAudioPlayer().src = src
		getCurrentAudioPlayer().load()
		getCurrentAudioPlayer().play()
		setup = true
	}
}
audioplayer1.onended = play
audioplayer2.onended = play

function playBtn() {
	if (!setup) {
		play()
	} else if (getCurrentAudioPlayer().paused) {
		getCurrentAudioPlayer().play()
	} else {
		getCurrentAudioPlayer().pause()
	}
}

window.onkeydown = (e) => {
	if (e.keyCode == 32) {
		playBtn()
		return false
	}
}

setInterval(() => {
	if (songlist.length < 30 && setup) {
		updateSongs(10)
	}
	if (getCurrentAudioPlayer().paused) {
		let playbtn = document.getElementById("playbuttonimg")
		playbtn.src = "play-icon.svg"
	} else {
		let playbtn = document.getElementById("playbuttonimg")
		playbtn.src = "pause-icon.svg"
	}
	progressbar.value = getCurrentAudioPlayer().currentTime
}, 100)

function settings() {
	document.location.href = document.location.href + "settings"
}