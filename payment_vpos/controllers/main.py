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

    @http.route('/bancard/return_url', type='json', auth='public', methods=['POST'], csrf=False, website=True)
    def vpos_bancard_return_url(self, **kw):
        _logger.info('Respuesta de Bancard (ok o error)')

        data = request.jsonrequest
        data = {
            "operation": {
                "token": "123456789/*",
                "shop_process_id": 46,
                "response": "S",
                "response_details": "Procesado satisfa",
                "amount": "1500.00",
                "currency": "PYG",
                "authorization_number": "6468542",
                "ticket_number": "65497684646",
                "response_code": "00",
                "response_description": "Transaccion aprobada",
                "extended_response_description": "null",
                "security_information": {
                    "customer_ip": "201.45.45.111",
                    "card_source": "L",
                    "card_country": "PARAGUAY",
                    "version": "0.3",
                    "risk_index": 0
                }
            }
        }
        ans = http.request.redirect('/bancard/show_answer')
        _logger.info('Redirected response')

        acquirer = request.env['payment.acquirer'].browse(14)
        return acquirer.sudo().render('/bancard/show_answer')

    @http.route('/bancard/show_answer', type='http', auth='public', csrf=False)
    def vpos_show_answer(self, **kw):
        _logger.info('answer response', str(kw))
        return http.request.render('payment_vpos.vpos_approved', kw)

    @http.route('/bancard/cancelled', type='json', auth='public', methods=['POST'], csrf=False)
    def vpos_bancard_cancelled(self, **kw):
        _logger.info('Respuesta de Bancard Cancelacion')
        return http.request.render('payment_vpos.vpos_cancelled', {})
