(function () {
'use strict';

var $xlog = {
    context_selector: "#instantlog",
    content: [],
    start: 0,
    page_size: 100,
    stop: -1,
    levels: {
        "NOTSET": 0,
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    },
    registered_modules: ['core', 'account', 'frontend', 'django', 'celery',],
    level: 10,
    module_name: "*",

    template: "<tr>" +
        "<td class='logtd'><%= module_name %></td> " +
        "<td class='logtd'><span class='log_<%= levelname %>'><%= levelname %></span></td> " +
        "<td class='logtd'> <%= xtime %></td>" +
        "<td class='logtd'><%= message %></td>" +
        "</tr>",

    add_message : function (message) {
        // console.log(message)
        if (message.message !== '_heartbeat_') {
            message.levelno = this.levels[message.levelname]
            message.xtime = message.asctime.substr(11, 8)
            this.content.push(message)
            this.render()
        }
    },
    set_level: function(level) {
        this.level = this.levels[$$.to_upper(level)];
        this.render();
        },
    set_module: function(module_name) {
        if (module_name === 'reset') {
            this.module_name = "*"
        }
        else {
            this.module_name = module_name
        }
        this.render();
    },
    first_index: function() { return 0 },
    last_index:  function() { return this.content.length - 1 },
    render: function () {
        var self = this,
            result = "",
            tmplist = []
        for (var i=this.last_index(); i>=this.first_index(); i-=1 ) {
            var item = this.content[i];
            if (item.levelno < this.level) {
                continue
            }
            if (this.module_name === 'other' && ! this.registered_modules.includes(item.module_name)) {
                // ok
            }
            else if (this.module_name !== "*" && item.module_name !== this.module_name) {
                continue
            }
            tmplist.push(item)
            if (tmplist.length >= this.page_size) {
               break
            }
        }
        tmplist.reverse().forEach(function (item) {
            result += _.template(self.template)(item)
        })
        $(this.context_selector).html(result)
    }
}

window.$xlog = $xlog;
// https://stackoverflow.com/questions/951791/javascript-global-error-handling
window.onerror = function(msg, url, line, col, error) {
    console.log("error")
}
}());
