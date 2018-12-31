
function getParameterByName(name, url) {
    if (!url) {
      url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function loadTweetContainer(tweetContainerID, fetchOneId){
  var query = getParameterByName('q')
  var tweetList = [];
  var nextTweetUrl;
  
  var tweetContainer;
  if (tweetContainerID){
    tweetContainer = $("#" + tweetContainerID)
  } else {
    tweetContainer = $("#tweet-container")
  }

  var initialURL = tweetContainer.attr("data-url") || "/api/post/";
  console.log("ok")


  $(document.body).on("click", ".tweet-like", function(e){
    e.preventDefault()
    var this_ = $(this)
    var tweetId = this_.attr("data-id")
    var likedUrl = '/api/post/' + tweetId + "/like/"
      // this_.text("Liked")
      $.ajax({
        method:"GET",
        url: likedUrl,
        success: function(data){
          if (data.liked){
            this_.text("Liked")
          } else {
            this_.text("Unliked")
          }
        },
        error: function(data){
          console.log("error")
          console.log(data)
        }

      })
    })

  $(document.body).on("click", ".tweet-reply", function(e){

    e.preventDefault()
    var this_ = $(this)
    var parentId = this_.attr("data-id")
    var username = this_.attr("data-user")
    var content = this_.parent().parent().find(".content").text()
    $("#replyModal").modal({})
    $("#replyModal textarea").after("<input type='hidden' value='" + parentId + "' name='parent_id' />")
    $("#replyModal textarea").after("<input type='hidden' value='" + true + "' name='reply' />")
    $("#replyModal textarea").val("@" + username + " ")
    $("#replyModal #replyModalLabel").text("Reply to " + content)
    $("#replyModal").on("shown.bs.modal", function(){
      $('textarea').focus()
    })
  })



  $(document.body).on("click", ".retweetBtn", function(e){

    e.preventDefault()
    console.log("clicked")
    var url = "/api" + $(this).attr("href")

    $.ajax({
      method: "GET",
      url: url,
      success: function (data) {
        console.log(data)
        // if username is in the API path... let's ignore 
        if (initialURL == "/api/post/") {
          attachTweet(data, true, true)
          updateHashLinks()
        }
        
      },
      error: function(data){
        console.log("error")
        console.log(data)
      }
    })
  })
  function updateHashLinks(){
    $(".content").each(function(data){
      var hashtagRegex = /(^|\s)#([\w\d-]+)/g
      var usernameRegex = /(^|\s)@([\w\d-]+)/g
      var currentHtml = $(this).html()
      var newText;
      newText = currentHtml.replace(hashtagRegex, "$1<a href='/tags/$2/'>#$2</a>")
      newText = newText.replace(usernameRegex, "$1 @<a href='/$2/'>$2</a>")
      $(this).html(newText)
    })
  }


  function formatTweet(tweetValue) {

    var preContent;
    var container;
    var tweetContent;
    var isReply = tweetValue.reply;
    var replyId = tweetValue.id 
    if (tweetValue.parent) {
      replyId = tweetValue.parent.id
    }

    var openingContainerDiv = "<div class=\"media\">"
    if (tweetValue.id == fetchOneId) {
      openingContainerDiv = "<div class=\"media media-focus\">"
      setTimeout(function(){
        $('.media-focus').css("background-color", '#fff')
      }, 2000)
    }

    if (tweetValue.parent && !isReply) {
        // there is a retwet
        tweetValue = tweetValue.parent
        preContent = "<span class='grey-color'>Retweet via " + tweetValue.user.username +" on " + tweetValue.date_display + "</span><br/>"
      } else if (tweetValue.parent && isReply) {
       preContent = "<span class='grey-color'>Reply to @" + tweetValue.parent.user.username +  "</span><br/>"
     }

     var verb = 'Like'
     if (tweetValue.did_like){
      verb = 'Unlike'
    }



    tweetContent = "<span class='content'>" + tweetValue.content
    + "</span><br/> via <a href='" + tweetValue.user.url + "'>"
    + tweetValue.user.username + "</a> | " + tweetValue.date_display
    + " | " + "<a href='/post/" + tweetValue.id + "'>View</a> | "
    + " | <a href='#' class='tweet-like' data-id='"
    + tweetValue.id + "''>" + verb + " (" + tweetValue.likes
    + ")</a>" + " | <a href='#' class='tweet-reply' data-user='" 
    + tweetValue.user.username + "' data-id='" + replyId
    + "''>Reply</a>"
    if (tweetValue.image_url != "") {
      tweetContent += 
                    ""//"| Image " + tweetValue.image_url
                    + "<img src=" + tweetValue.image_url + " class='img-responsive' />"
    }

    if (preContent) {
      container= openingContainerDiv + "<div class=\"media-body\">" + preContent + tweetContent + "</div></div><hr/>"
    } else {
      container = openingContainerDiv + "<div class=\"media-body\">" + tweetContent + "</div></div><hr/>"
    }

   return container
 }
 
 function attachTweet(tweetValue, prepend, retweet){

  tweetFormattedHtml = formatTweet(tweetValue)

  if (prepend==true){
    tweetContainer.prepend(tweetFormattedHtml)
  } else {
    tweetContainer.append(tweetFormattedHtml)
  }
}

function parseTweets(){
  if (tweetList == 0) {
    tweetContainer.text("No tweets currently found.")
  } else {
      // tweets exist, parse & display them
      $.each(tweetList, function(key, value){
        var tweetKey = key;
        if (value.parent) {
          attachTweet(value, false, true)
        } else {
          attachTweet(value)
        }

      })
    }
  }

  function fetchTweets(url){
    console.log('fetching')
    var fecthUrl;
    if (!url) {
      fecthUrl = initialURL
    } else {
      fecthUrl = url
    }
    $.ajax({
      url: fecthUrl,
      data: {
        "q": query
      },
      method: "GET",
      success: function(data){
        // console.log(data)
        tweetList = data.results
        if (data.next){
          nextTweetUrl = data.next
        } else {
          $("#loadmore").css("display", "none")
        }
        parseTweets()
        updateHashLinks()

      },
      error: function(data){
        console.log("error")
        console.log(data)
      }
    })
  }

  function fetchSingle(fetchOneId){
    var fecthDetailUrl = '/api/post/' + fetchOneId + '/'
    console.log(fecthDetailUrl)
    $.ajax({
      url: fecthDetailUrl,
      method: "GET",
      success: function(data){
       console.log(data)
       tweetList = data.results
        // if (data.next){
        //   nextTweetUrl = data.next
        // } else {
        //   $("#loadmore").css("display", "none")
        // }
        parseTweets()
        updateHashLinks()

      },
      error: function(data){
        console.log("error")
        console.log(data)
      }
    })
  }


  if (fetchOneId){
    fetchSingle(fetchOneId)
  } else {
    fetchTweets()
  }
  


  $("#loadmore").click(function(event){
    event.preventDefault()
    if (nextTweetUrl) {
      fetchTweets(nextTweetUrl)
    }
      // load more items
    })
  
  var charsStart = 140;
  var charsCurrent = 0;

  $(".tweet-form").append("<span class='tweetCharsLeft' style='margin-left: 20px'>" + charsStart + " left</span>")

  $(".tweet-form textarea").keyup(function(event){
    var tweetValue = $(this).val()
    charsCurrent = charsStart - tweetValue.length
    var spanChars = $(this).parent().parent().parent().find("span.tweetCharsLeft")
    spanChars.text(charsCurrent)

    if (charsCurrent > 0 ) {
         // remove classes
         spanChars.removeClass("grey-color")
         spanChars.removeClass("red-color")
       } else if (charsCurrent == 0) {
         // add grey class
         spanChars.removeClass("red-color")
         spanChars.addClass("grey-color")
       } else if (charsCurrent < 0) {
          // add red class
          spanChars.removeClass("grey-color")
          spanChars.addClass("red-color")
        }

      })

  $(".tweet-form").submit(function(event){
    event.preventDefault()
    var this_ = $(this)
    //var formData =  this_.serialize()
    var formData = new FormData(this_[0]);
    //console.log(formData)
    //var image_file = document.getElementById('id_image')
    //console.log(image_file)
    if (charsCurrent >= 0) {
      $.ajax({
        url: "/api/post/create/",
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        method: "POST",
        success: function(data){
          this_.find("input[type=text], textarea").val("")
          attachTweet(data, true)
          updateHashLinks()
          $("#replyModal").modal("hide")
        },
        error: function(data){
          console.log("error")
          console.log(data.statusText)
          console.log(data.status)
        }
      })
    }  else {
      console.log("Cannot send, tweet too long.")
    }




  })
}