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
        _logger.info('Enviando peticion a bancard')
        return http.request.render('payment_vpos.vpos_iframe', {
                "iframe_url": kw.get('url')
            })

    @http.route('/bancard/error', type='http', auth='public', csrf=False)
    def vpos_bancard_error(self, **kw):
        _logger.error('Error interno al procesar datos')
        return http.request.render('payment_vpos.vpos_error', {})

    @http.route('/bancard/return_url', type='http', auth='public', csrf=False)
    def vpos_bancard_return_url(self, **kw):
        _logger.info('Respuesta de Bancard (ok o error)')
        return http.request.render('payment_vpos.vpos_approved', {})

    @http.route('/bancard/cancelled', type='http', auth='public', csrf=False)
    def vpos_bancard_cancelled(self, **kw):
        _logger.info('Respuesta de Bancard Cancelacion')
        return http.request.render('payment_vpos.vpos_cancelled', {})
