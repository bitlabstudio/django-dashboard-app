(function ($) {

"use strict";

var interval;

function init() {
    interval = setInterval(find_outdated, 60000);
    find_outdated();
}

function find_outdated() {
    $.get(get_outdated_url, function(data) {
        for (var i = 0; i < data.length; i++) {
            reload_widget(data[i]);
        }
    });
}

function reload_widget(widget_name) {
    // TODO
}

$(document).ready(init);

}(jQuery))
