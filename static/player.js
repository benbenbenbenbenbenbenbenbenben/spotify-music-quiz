
const playBtn = document.getElementById('btn-play-pause')
const nextBtn = document.getElementById("next")
const songNum = document.getElementById("songNum")
const songDetails = document.getElementById("songDetails")
const coverImg = document.getElementById("coverImg")
const coverText = document.getElementById("coverText")
const artist = document.getElementById("artist")
const devicesDropdown = document.getElementById("dropdown-devices")
const song_progress = document.getElementById("song_progress")
const bg = document.getElementById("bg")
const volume = document.getElementById("volume")

let songCounter = 1

// Listen for animation start/end
song_progress.onanimationstart = () => {
    nextBtn.classList.remove('flash')
}
song_progress.onanimationend = () => {
    nextBtn.classList.add('flash')
}


async function first_song(data){
    let response = await fetch("/song/"+data.track.id)
    let state = await response.json()
    songNum.innerHTML = songCounter++
    toggle_play(state)
    song_progress.classList.remove('stop')
}

async function next_song(category){
    song_progress.classList.add('stop')
    let response = await fetch("/quiz?next="+category)
    let data = await response.json()
    img_colour(data.track.album.images[0].url, 'Vibrant', bg)
    img_colour(data.track.album.images[0].url, 'DarkMuted', coverImg)
    response = await fetch("/song/"+data.track.id)
    let state = await response.json()
    toggle_play(state)
    song_progress.classList.remove('stop')
    songNum.innerHTML = songCounter++
}

async function get_next_song(){
    song_progress.classList.add('stop')
    let butId = currentCatX + 1
    let activeCheck = document.getElementById("buttonCategory"+butId).classList.contains("btn-success")
    //Check End Of Category
    if(currentTrackX == 0 && !activeCheck){
        category(currentCatX+1)
        
    } else {
        let song = data.quiz.categories[currentCatX].category_tracks[currentTrackX].track
        let response = await fetch("/song/"+song.id)
        songDetails.innerHTML = song.name
        artist.innerHTML = song.artists[0].name
        coverImg.style.background = "url('"+song.album.images[0].url+"')"
        img_colour(song.album.images[0].url, 'Vibrant', bg)
        coverImg.style.backgroundSize = "400px 300px"
        coverText.innerHTML = ""
        let state = await response.json()
        toggle_play(state)
        song_progress.classList.remove('stop')
        console.log(state)
        currentTrackX++
        currentTrack.innerHTML = currentTrackX
        currentCat.innerHTML = currentCatX + 1
        if (currentTrackX == data.quiz.categories[currentCatX].category_tracks.length ){
            currentCatX++
            currentTrackX = 0
        }
    }
}

async function play_pause(){
    let response = await fetch('/player/play_pause')
    let state = await response.json()
    toggle_play(state)
}

async function pause(){
    let response = await fetch('/player/pause')
    let state = await response.json()
    toggle_play(state)
}

async function category(id){
    //Pause Previous Song
    pause()
    //Remove Old Active Button
    let buttons = document.getElementsByClassName("btn-success")
    if(buttons[0]){
        buttons[0].classList.add("btn-dark")
        buttons[0].classList.remove("btn-success") 
    }
    //Add Active Button
    let button = document.getElementById("buttonCategory"+id)
    button.classList.remove("btn-dark")
    button.classList.add("btn-success")
    //Set Counters
    id >0 ? id-- : 0
    currentCatX = id
    currentCat.innerHTML = currentCatX
    currentTrackX = 0
    currentTrack.innerHTML = 0
    totalTrack.innerHTML = data.quiz.categories[id].category_tracks.length
    songDetails.innerHTML = "-"
    artist.innerHTML = data.quiz.categories[id].category_name
    coverImg.style.backgroundImage = "none"
    coverImg.style.backgroundColor = random_color()
    coverText.innerHTML = button.innerHTML
    resize_text()
}
// Update Play Button If Playing or Paused
function toggle_play(state){
    console.log(state)
    if (state.state == 'playing'){
        playBtn.classList.remove('fa-play')
        song_progress.classList.remove('pause')
        playBtn.classList.add('fa-pause')
    } else {
        playBtn.classList.remove('fa-pause')
        playBtn.classList.add('fa-play')
        song_progress.classList.add('pause')
    }
}
// List Of Devices Spotify Can Play To
async function devices(action){
    let response = await fetch('/devices/list')
    let devices = await response.json()
    console.log(devices)
    // Return Devices
    if(action == 'get'){
        let items = ''
        for (device of devices.devices){
            if (device.is_active){
                items += '<span onclick="transfer_device(\''+device.id.toString()+'\')" class="dropdown-item alert alert-success">'+device.name+'</span>'
            } else {
                items += '<span onclick="transfer_device(\''+device.id.toString()+'\')" class="dropdown-item alert alert-secondary">'+device.name+'</span>'
            }
        }
        devicesDropdown.innerHTML = items
        return devices.devices[0].id
    }
    // Return Volume Of Active Device
    else if(action == 'volume'){
        for (device of devices.devices){
            if (device.is_active){
                volume.value = device.volume_percent
                adjust_volume_slider()
            }
        }
    }
}
// Transfer Playback To Another Device
async function transfer_device(device_id){
    let response = await fetch('/devices/transfer?device='+device_id)
}

// Resize Text To Fit Cover Image
function resize_text(){
    let element = document.getElementById('coverText')
    //reset padding
    element.style.padding = "0"
    let height = element.offsetHeight
    let fontSize = parseInt(element.style.fontSize)
    while ( height > 300 ) {
        fontSize = fontSize - 10
        element.style.fontSize = fontSize + "px"
        height = element.offsetHeight
    }
    element.style.padding = ((300 - height)/2)+"px 0"
}

// Random Color
function random_color(){
    let randomColor = Math.floor(Math.random()*16777215).toString(16);
    return "#" + randomColor
}

async function adjust_volume(value){
   let response = await fetch('/player/volume?volume='+value)
   adjust_volume_slider()
}

function img_colour(img, mode, element){
    //https://jariz.github.io/vibrant.js/
    Vibrant.from(img).getPalette().then(function(palette) {
        if (palette[mode]._rgb){
            let colours = palette[mode]._rgb
            element.style.backgroundColor = 'rgb('+colours[0]+','+colours[1]+','+colours[2]+')'
        }
    })
}

// Listen For Volume Changes
function adjust_volume_slider() {
    let val = ($(volume).val() - $(volume).attr('min')) / ($(volume).attr('max') - $(volume).attr('min'));
    $(volume).css('background-image',
                '-webkit-gradient(linear, left top, right top, '
                + 'color-stop(' + val + ', #32cd32), '
                + 'color-stop(' + val + ', #fff)'
                + ')'
                )
}