$("#login-btn").click(function(){      
    console.log("I am hereeee")
    $.ajax({
    url: "/login-submit/",
    type: "POST",
    headers:{
        'X-CSRFToken':getCsrfToken()
    },
    data: {
        username: $("#username").val(),
        password: $("#password").val()
    },
    success: function(response) {
        console.log("Success!", response);
        
        if(response["status"]==200)
        {
            console.log("Success!!!")
            console.log(response["usertype"])
        // window.location.pathname = "/home"
        }
        else
        {
        alert( "The username or password is incorrect!");
        }
    },
    error: function(xhr, textstatus, errorthrown) {
        console.log("Please report this error: "+errorthrown+xhr.status+xhr.responseText);
    }
    });
});