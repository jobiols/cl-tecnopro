# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class VPosController(http.Controller):

    @http.route('/payment/vpos/response', type='http', auth='public', csrf=False)
    def vpos_response(self, **post):
        """ vPOS."""
        _logger.info('vPOS: entering form_feedback with post response data %s', pprint.pformat(post))
        if post:
            request.env['payment.transaction'].sudo().form_feedback(post, 'vpos')
        return werkzeug.utils.redirect('/payment/process')
