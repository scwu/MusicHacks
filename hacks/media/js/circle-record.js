var circleUrl = document.URL;
console.log(circleUrl);

      function timecode(ms) {
        var hms = {
          h: Math.floor(ms/(60*60*1000)),
          m: Math.floor((ms/60000) % 60),
          s: Math.floor((ms/1000) % 60)
        };
        var tc = []; // Timecode array to be joined with '.'
        if (hms.h > 0) {
          tc.push(hms.h);
        }
        tc.push((hms.m < 10 && hms.h > 0 ? "0" + hms.m : hms.m));
        tc.push((hms.s < 10  ? "0" + hms.s : hms.s));
        return tc.join(':');
      }
    

      Recorder.initialize({
        swfSrc: "../../media/recorder.js/recorder.swf"
      });

      function record(){
        Recorder.record({
          start: function(){
            //alert("recording starts now. press stop when youre done. and then play or upload if you want.");
          },
          progress: function(milliseconds){
            //document.getElementById("time").innerHTML = timecode(milliseconds);
          }
        });
      }
      
      function play(){
        Recorder.stop();
        Recorder.play({
          progress: function(milliseconds){
            //document.getElementById("time").innerHTML = timecode(milliseconds);
          }
        });
      }
      
      function stop(){
        Recorder.stop();
      }
      
      function upload(){
        SC.connect({
          client_id: "aHT5HITYm8vlkWNabL0Qg",
          redirect_uri: circleUrl,
          connected: function(){
            Recorder.upload({
              url:        "https://api.soundcloud.com/tracks.json?oauth_token=" + SC.options.access_token,
              audioParam: "track[asset_data]",
              params: {
                "track[title]":   "recorder.js track test",
                "track[sharing]": "private"
              },
              success: function(responseText){
                var track = $.parseJSON(responseText)
                window.location = track.permalink_url;
              }
            });
          },
          error: function(err){
            alert(err)
          }
        })
      }