# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class VPosController(http.Controller):

    @http.route('/bancard', type='http', auth='public', csrf=False)
    def vpos_bancard(self, **kw):
        return http.request.render('payment_vpos.vpos_iframe', {
                "iframe_url": kw.get('url')
            })

    @http.route('/bancard_error', type='http', auth='public', csrf=False)
    def vpos_bancard_error(self, **kw):
        return http.request.render('payment_vpos.vpos_error', {})
