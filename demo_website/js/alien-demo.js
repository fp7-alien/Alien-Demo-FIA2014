var vlc = document.getElementById("alienPlayer");
var infoWindow = document.getElementById("info");
var linkStatusWindow = document.getElementById("link-status");
var buttonConnect = document.getElementById("connect");
var buttonDisconnect = document.getElementById("disconnect");
var state = "stop";
var disconnect = false;
var connect = false;

function togglePlayCtrl () {
  if ( $("#play-ctrl").is( ":hidden" ) ) {
    $("#play-ctrl").children().slideDown();
  } else {
    $("#play-ctrl").children().slideUp();
  }
}

function toggleDisable() {
  $('#conn').prop("disabled",!$('#conn').prop("disabled"))
}

function disableConn() {
  $('#conn').attr("disabled", true);
}

function enableConn() {
  $('#conn').attr("disabled", false);
}

function play() {
  vlc.playlist.play();
  state="start";
}

function pause() {
  vlc.playlist.togglePause();
  state="pause";
  if (vlc.input.state == "4") {
    state="play";
  }
}

function stop() {
  vlc.playlist.stop();
  state="stop";

}

function checkState() {
  vlc.playlist.play();
  state="self-start"
}

function showConnect() {
  $('#conn').html('<span class="glyphicon glyphicon-flash"></span>Connect'); 
  $('#conn').attr("class","btn btn-success btn-lg");
  $('#conn').attr("onclick","javascript:doGET('connect');");
}

function showDisconnect() {
  $('#conn').html('<span class="glyphicon glyphicon-remove"></span>Disconnect');
  $('#conn').attr("class","btn btn-danger btn-lg");
  $('#conn').attr("onclick","javascript:doGET('disconnect');");
}

$(document).ready(function () {
            start_timer = setInterval(function () {
              var s = vlc.input.state;
              infoWindow.innerHTML=s+" - "+state;
              if (s=='3' && state=="self-start") {  // link up -> pause
                vlc.playlist.togglePause();
                ////toggleDisable();
                togglePlayCtrl();
                enableConn();
                showDisconnect();
                infoWindow.setAttribute("class", "label label-success");
                $('#link-status').attr("class","label label-success");
                $('#link-status').text("Link up");
                state="pause";
                buttonDisconnect.disabled=false;
                buttonConnect.disabled=true;
              } else if (s=="7" && state=="self-start" && disconnect==false) { // link down -> check again
                buttonDisconnect.disabled=true;
                if (connect==true) {
                  buttonConnect.disabled=true;
                  ////toggleDisable();
                  disableConn();
                } else {
                  buttonConnect.disabled=false;
                  showConnect();
                  //toggleDisable();
                  enableConn();
                }
                vlc.playlist.stop();
                infoWindow.setAttribute("class", "label label-danger");
                $('#link-status').attr("class","label label-danger");
                if (connect) {
                  $('#link-status').text("Link down - connecting...");
                } else {
                  $('#link-status').text("Link down");
                }
                checkState();
              } else if (s=="6" && disconnect==true) {  // disconnecting -> waiting for player error
                vlc.playlist.stop();
                togglePlayCtrl();
                showConnect();
                ////toggleDisable();
                enableConn();
                infoWindow.setAttribute("class", "label label-danger");
                $('#link-status').attr("class","label label-danger");
                $('#link-status').text("Link down");
                disconnect=false;
                buttonDisconnect.disabled=true;
                buttonConnect.disabled=false;
              }
            },
        1000);
        });


function doGET(msg) {
  if (msg=="connect") {
    $.ajax({
      url: "http://10.0.0.200",
      timeout: 500
    });
    $.ajax({
      url: "http://192.168.0.200",
      timeout: 500
    });
    connect=true;
    buttonConnect.disabled=true;
    ////toggleDisable();
    disableConn();
    $("#link-status").append(' - connecting...');
    checkState();
  } else if (msg=="disconnect") {
    $.ajax({
      url: "http://10.0.0.201",
      timeout: 500
    });
    $.ajax({
      url: "http://192.168.0.201",
      timeout: 500
    });
    buttonDisconnect.disabled=true;
    ////toggleDisable();
    disableConn();
    $("#link-status").append(' - disconnecting...');
    disconnect = true;
  }
}

$(document).keydown(function(event) {
  if (event['which']==65) {
    $( "#info" ).toggle();
    $( "#connect" ).toggle();
    $( "#disconnect" ).toggle();
  }
});

checkState();