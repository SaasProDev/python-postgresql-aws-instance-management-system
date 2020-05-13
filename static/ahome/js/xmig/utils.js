// Set of utilities
// copyright - Sergii Tretiak (tretyak@gmail.com)- MIT License.
// Suppose using jQuery

(function () {
    'use strict';

var $$ = {
    last_unique_id: null,
    get_random_as_sting : function () {
        return ("" + Math.random()).replace(/\./g, '');
    },

    is_defined : function (value) {
        return typeof(value) !== 'undefined' && value !== null
    },

    to_lower: function(value) {
         if ($$.is_string(value)) {
             return value.toLowerCase();
         }
         return ""
    },
    to_upper: function(value) {
         if ($$.is_string(value)) {
             return value.toUpperCase();
         }
         return ""
    },
    is_true : function (value) {
        var val;
        if($$.is_defined(value)) {
            if ($$.is_string(value)) {
                val = value.toUpperCase();
                if (val === 'Y' || val === 'YES' || val === 'TRUE') {
                    return true
                }
            }
            else {
                val = Number(value);
                if(val) {
                    return val !== 0
                }
            }
        }
        return value === true;
    },
    random_int_interval: function(min, max) {
        return Math.floor(Math.random()*(max-min+1)+min);
    },
    random_int: function(max) {
        return $$.random_int_interval(0, max);
    },
    random_array: function(input_array, items_count) {
        var result = [],
            current_length = input_array.length,
            temp_array = input_array.slice(0);

        items_count = $$.is_defined(items_count)
            && current_length > items_count
            ? items_count : current_length;

        for (var i=1; i<=current_length; i+=1) {
            var ind = $$.random_int(current_length-i);
            result.push(temp_array.splicesplice(ind, 1)[0]);
        }
        return result;
    },
    get_dotted_value: function(key, dict) {
        if (! $$.is_object(dict)) {
            return dict
        }

        var idx = key.indexOf(".");
        if (idx === -1) {
            return dict[key];
        }
        var a = key.substring(0, idx),
            b = key.substring(idx + 1);

        return this.get_dotted_value(b, dict[a])
    },
    as_bool: function (value) {
        return "" + value === 'true'
    },
    is_string : function (value) {
        return (typeof value === 'string' && value.length > 0)
    },
    is_function : function (value) {
        return $$.is_defined(value) && (typeof value === 'function')
    },
    is_object : function (value) {
        return $$.is_defined(value) && (typeof value === 'object')
    },
    is_array: function(value) {
        return Array.isArray(value)
    },
    includes: function(arr, value) {
      return $$.is_array(arr) ? arr.includes(value) : false
    },
    index_of: function(arr, value) {
      return $$.is_array(arr) ? arr.indexOf(value) : -1
    },
    shift_element: function(arr, element_index, relative_position) {
        // todo refactor this ugly code
      if ( relative_position === 0
          || (arr.length <= element_index + relative_position)
          || (0 > element_index + relative_position)) {
        return arr
      }

      var value = arr[element_index],
          before = arr.slice(0, element_index),
          after = arr.slice(element_index+1, arr.length),
          v = null,
          tmp = null;

      if (relative_position > 0) {
          v = after.shift();
          tmp = before.concat();
          tmp.push(v);
          tmp.push(value);
          return tmp.concat(after)
      }
      else {
        v = before.pop();
        before.push(value);
        before.push(v);
        return before.concat(after);
      }
    },
    as_id_selector : function (name) {
        return name[0] === "#" ? name: "#" + name;
    },
    as_plain_id : function (name) {
        return name[0] === "#" ? $$.skip_first_char(name):  name;
    },

    as_class_selector : function (name) {
        return name[0] === "." ? name: "." + name;
    },
    object_keys: function(obj) {
        return $$.is_object(obj) ? Object.keys(obj) : []
    },
    deep_copy: function(obj) {
        return JSON.parse(JSON.stringify(obj));
    },
    clone_object : function(destination, source, required_fields, except_fields_list) {
        // does not support FULL clone features for now
        except_fields_list = $$.is_defined(except_fields_list) ? except_fields_list : [];
        for (var field in source) {
            if ($.inArray(field, required_fields) !== -1 && $.inArray(field, except_fields_list) === -1) {
                if ($$.is_defined(source[field]) && $$.is_object(source[field])) {
                    if ($$.is_array(source[field])) {
                    }
                    else {
                        $$.clone_object(destination[field], source[field]);
                    }
                }
            }
            else {
                destination[field] = source[field];
            }
        }
        return destination
    },
    update_object : function(destination, source) {
        return $$.clone_object(destination, source);
    },
    unique_id : function(base_id) {
        base_id = $$.is_defined(base_id) ? base_id + "_" : "";
        var random_str = "" + Math.random(),
            random_id = "" + base_id + random_str.substring(2, 8);
        this.last_unique_id = random_id;
        return random_id;
    },

    as_id : function(base_id, ext) {
        return base_id + "_" + ext;
    },

    clear_id : function (name) {
        return ($$.is_string(name) && name[0] === '#') ? name.substr(1) : name;
    },

    as_array : function(str, splitter) {
        var result = [];
        var arr = str.split($$.is_string(splitter) ? splitter : " ");
        for(var i in arr) {
            result.push(arr[i].trim());
        }
        return result;
    },
    contains_string: function(wrap_string, substring) {
        return $$.is_string(wrap_string) && wrap_string.indexOf(substring) !== -1
    },
    first_word: function(str) {
        var a = this.as_array(str, ",");
        return a ? a[0] : str;
    },

    last_char : function (str) {
        return $$.is_string(str) ? str[str.length-1] : undefined;
    },
    first_char : function (str) {
        return $$.is_string(str) ? str[0] : undefined;
    },
    first_chars : function(val, count) {
        val = "" + val;
        return val.slice(0, count)
    },
    last_chars : function(val, count) {
        val = "" + val;
        return val.slice(-count)
    },
    skip_first_char : function (str) {
        return str.substr(1, str.length);
    },
    skip_last_digit_from_name : function (str) {
        var ch = $$.last_char(str);
        return ch >= '0' && ch <= '9' ? str.substr(0, str.length-1) : str;
    },

    is_last_char_01 : function (name) {
        var ch = $$.last_char(name);
        return ch === '0' || ch === '1' ? ch : -1;
    },
    join_url : function(prefix, suffix) {
        prefix = $$.last_char(prefix)  === '/' ? prefix : prefix + "/";
        suffix = $$.first_char(suffix) === '/' ? $$.skip_first_char(suffix) : suffix;
        return prefix + suffix;
    },
    swap_char_01 : function (ch) {
        return (ch === '0')
            ? '1'
            : ((ch === '1')
                ? 0
                : ch);
    },
    join_array: function(arr, separator) {
        return arr.join(separator)
    },
    swap_last_char_01 : function (str) {
        return str.substr(0, str.length-1) + $$.swap_char_01($$.last_char(str));
    },

    switch_class : function (element, class_name) {
       if (element.hasClass(class_name)) {
           element.removeClass(class_name)
       }
       else {
           element.addClass(class_name)
       }
       return element
    },
    filtered_fields: function(obj, interesting_fields) {
        var result = {};
        for (var i=0; i<interesting_fields.length; i+=1) {
            var field_name = interesting_fields[i];
            if ($$.is_defined(obj[field_name])) {
                result[field_name] = obj[field_name]
            }
        }
        return result
    },

/*
Toggle ALL class names "xxx0" <--> "xxx1"
Applied only if name is '1' or '0' terminated
 */
    toggle_item_01 : function(js_obj) {
        var html = $$.getOuterHTML(js_obj),
            jq_obj = $(js_obj),
            regexp = /class=\"(.*?)\"/;

        regexp.test(html);
        var arr = RegExp.$1.split(' ');

        for (var i = 0; i < arr.length; ++i) {
            var cls = arr[i];
            jq_obj.removeClass(cls);
            jq_obj.addClass($$.swap_last_char_01(cls));
        }
    },
    toggle_class(element, class_1, class_2) {
        var e = $(element);
        if (e.hasClass(class_1)) {
            e.removeClass(class_1).addClass(class_2);
            return 1;
        }
        if (e.hasClass(class_2)) {
            e.removeClass(class_2).addClass(class_1);
            return 2;
        }
        return 0
    },
    toggle_visible: function (element) {
        if (element.style.display === "none") {
            element.style.display = "block";
        } else {
            element.style.display = "none";
        }
    },

    trim: function(str) {
        return this.is_defined(str) ? str.replace(/^\s+|\s+$/g, '') : '';
    },
    normalise_url: function(str) {
         return this.is_defined(str) ? str.replace(new RegExp("/{2,}",'g'),"/") : '';

    },
    replace_word: function(str, source_word, target_word) {
         return this.is_defined(str) ? str.replace(new RegExp(source_word,'g'), target_word) : '';

    },
    setOuterHTML: function(node, html) {
        if (node.outerHTML) {
            node.outerHTML = html;
        }
        else {
            var range = document.createRange();
            range.setStartBefore(node);
            var fragment = range.createContextualFragment(html);
            item.parentNode.replaceChild(fragment, node);
        }
        return node
    },

    getOuterHTML: function(node) {
        var html = node.outerHTML;
        if ( ! $$.is_defined()) {
            if ($$.is_defined(node.parentNode) && node.parentNode.nodeType === 1) {
                var el = document.createElement(node.parentNode.nodeName);
                el.appendChild(node.cloneNode(true));
                html = el.innerHTML;
            }
        }
        return html
    },

    first_not: function(str, ch) {
        if ($$.is_string(str)) {
            var size = str.length -1;
            for (var i = 0; i < size; ++i) {
                if (str[i] !== ch) {
                    return i
                }
            }
        }
        return -1
    },

    last_not: function(str, ch) {
        if ($$.is_string(str)) {
            var size = str.length -1;
            for (var i = size; i >= 0; --i) {
                if (str[i] !== ch) {
                    return i
                }
            }
        }
        return -1
    },
    is_multi_line_string: function(text) {
            return /\r|\n/.exec(text);
    },

    open_window_creator: function(name, href, sizeX, sizeY) {
        return function () {
            return window.open(href, name, 'scrollbars=1'
                + ',height='+Math.min(sizeY, screen.availHeight)
                + ',width='+Math.min(sizeX, screen.availWidth));
        }
    },

    check_pop_up: function(name, constructor, reopen_anyway) {
        if (! window.mypopup) {
            window.mypopup = {}
        }

        if (window.mypopup[name] && window.mypopup[name].closed) {
            window.mypopup[name] = false
        }
        if (! window.mypopup[name] || $$.is_defined(reopen_anyway)) {
            window.mypopup[name] = constructor();
        }
        return window.mypopup[name]
    },

    scan_forms_element(form_id, success) {
        var elements = document.getElementById(form_id).elements;
        for (var i=0; i< elements.length; i+=1) {
            success($(elements[i]), i)
        }
    },
    set_css_var(var_name, var_value) {
        document.documentElement.style.setProperty(var_name, var_value);
    },
    get_css_var(var_name) {
        var styles = window.getComputedStyle($("html"));
        return styles.getPropertyValue(var_name)
    },
    get_attr(el, name) {
        return $(el).attr(name);
    },
    set_attr(el, name, value) {
        el = $(el);
        el.attr(name, value);
        return el
    },
    get_element_text(el) {
        return this.trim($(el).text());
    },
    set_element_text(el, text) {
        return $(el).text(text);
    },
    now() {
        return Date.now()
    },
    array_intersection(arr1, arr2) {
        return arr1.filter(function (n) {
            return arr2.indexOf(n) > -1;
        });
    },
    object_attr(obj, attr_name, default_value) {
        if ($$.is_object(obj)) {
            if ($$.is_defined(obj[attr_name])) {
                return obj[attr_name]
            }
        }
        return default_value
    }
};

window.$$ = $$;

}());

