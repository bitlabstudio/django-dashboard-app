(function ($) {

"use strict";

var interval;

function init() {
    interval = setInterval(find_outdated, 60000);
    find_outdated();
}

function find_outdated() {
    $.get(get_last_updates_url, function(data) {
        // We expect a dict of widget_names and last update times
        for (var widget_name in data) {
            // We have saved the latest last update time in a hidden field
            var last_update = $('#' + widget_name).find('.lastUpdate').val();
            if (last_update != data[widget_name]) {
                // We compare the latest last update time with the one returned
                // by the AJAX call. If it is different, we re-render the
                // widget
                reload_widget(widget_name);
            }
        }
    });
}

function reload_widget(widget_name) {
    var get_data = {'name': widget_name};
    $.get(render_widget_url, get_data, function(data) {
        $('#' + widget_name).replaceWith(data);
    });
}

$(document).ready(init);

}(jQuery))
