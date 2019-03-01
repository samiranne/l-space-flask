"use strict";

$( document ).ready(function() {
    // REMOVE FLASH MESSAGE ON CLICK
    $( ".flash-dismiss" ).click(function() {
        $(this).parent().remove();
    });

    // SET CLASS AS 'SELECTED' FOR CLICKED NAVBAR LINKS
    $("#navigation_links a").click(function() {
        $("#navigation_links a").removeClass("selected");
        $(this).addClass("selected");
    });

});