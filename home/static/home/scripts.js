// index.html mount calculator script
angular.module('mount_calculator', []).controller('MountCalculator', function(){
    this.p = 1.00;  //chance
    this.k = 1;     //number of drops
    this.n = 100;   //number of kills

    //binomial distribution
    this.drop_chance = function drop_chance_f(k, n, p){
        p = p/100
        var result = binom(n, k) * Math.pow(p, k) * Math.pow((1 - p), (n - k))

        result = result * 100;
        result = Math.round(result * 1000) / 1000; //3 decimals

        return (result + " %");
    };

    this.drop_chance_one = function drop_chance_f(k, n, p){
        p = p/100
        var result = binom(n, k) * Math.pow(p, k) * Math.pow((1 - p), (n - k))

        result = 1- result;
        result = result * 100;
        result = Math.round(result * 1000) / 1000;

        return (result + " %");
    };

    //http://rosettacode.org/wiki/Evalate_binomial_coefficients#JavaScript
    function binom(n, k) {
        var coeff = 1;
        for (var i = n-k+1; i <= n; i++) coeff *= i;
        for (var i = 1;     i <= k; i++) coeff /= i;
        return coeff;
    }
});

// roster.html jquery script
var $rows = $('#roster_table tbody tr');
$('#roster_search').keyup(function() {
    var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
    $rows.show().filter(function() {
        var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
    }).hide();
});

// index.html raid progression accordion script
$(function() {
    $( "#accordion" ).accordion({
        collapsible: true,
        active: false,
        heightStyle: "content"
    });
});

// news article div
function showDiv() {
    document.getElementById('edit_form').style.display = "block";
    document.getElementById('article_edit_button').style.display = "none";
    document.getElementById('article_delete_button').style.display = "none";
}

// ajax script
$(function() {


    // Submit post on submit
    $('#post-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_post();
    });

    // Delete post on click
    $(".chat_delete").on('click', 'a[id^=delete-post-]', function(event){
        event.preventDefault();
        var post_primary_key = $(this).attr('id').split('-')[2];
        console.log("PK: " + post_primary_key) // sanity check
        delete_post(post_primary_key);
    });

     // AJAX for deleting
    function delete_post(post_primary_key){
        if (confirm('are you sure you want to remove this post?')==true){
            $.ajax({
                url : "/delete_post/", // the endpoint
                type : "DELETE", // http method
                data : { postpk : post_primary_key }, // data sent with the delete request
                success : function(json) {
                    // hide the post
                  $('#chat-'+post_primary_key).hide(); // hide the post on success
                  console.log("post deletion successful");
                },

                error : function(xhr,errmsg,err) {
                    // Show an error
                    if(err == "FORBIDDEN"){
                        alert("Forbidden. You aren't supposed to be here, buddy.");
                    }else{
                        alert("Oops! Something went wrong. " + err);
                    }
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        } else {
            return false;
        }
    };

    // FROM DJANGO DOCS
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});