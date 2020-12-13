​​odoo.define('payment_vpos.bancard', function (require) {
    'use strict';

    var core = require('web.core');
    var sAnimation = require('website.content.snippets.animation');

    var _t = core._t;
    var ajax = require(web.ajax);

    sAnimation.registry.js_send_json_request = sAnimation.Class.extend({
    function (require) {
        ajax.jsonRpc("/bancard/return_url", 'call', {}).done(function() {
        }).then(function (json_data) {
            self.DataView.$el.append(QWeb.render('payment_vpos.show_answer',
            {'data': json_data}))
            // $("#ViewCartModal").modal(); // Display modal
            return ;
            })
        }
    })
})
