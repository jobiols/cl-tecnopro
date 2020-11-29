# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug
import pprint

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

#   @http.route('/bancard/return_url', type='json', auth='public', methods=['POST'], csrf=False, website=True)
    @http.route('/bancard/return_url', type='json', auth='public', csrf=False, website=True)
    def vpos_bancard_return_url(self, **kw):
        _logger.info('-----------------------------------------------------------------')

        # obtener los datos enviados por bancard despues de la transaccion
        data = request.jsonrequest
        _logger.info('Respuesta de Bancard (ok o error), \n%s',  pprint.pformat(data))


        # esto da este error 'JsonRequest' object has no attribute 'render'
        #ans = http.request.render('payment_vpos.show_answer', {})
        #_logger.info('Redirected response %s', ans.response)
        werkzeug.request.render('payment_vpos.show_answer', {})


        #acquirer = request.env['payment.acquirer'].browse(14)

        #reference = '/bancard/show_answer'
        #amount = float(data['operation']['amount'])
        #currency_id = False
        #values = data
        #acquirer.sudo().render(reference, amount, currency_id, partner_id=False, values=None)

        return

    @http.route('/bancard/show_answer', type='http', auth='public', csrf=False)
    def vpos_show_answer(self, **kw):
        _logger.info('answer response', str(kw))
        return http.request.render('payment_vpos.vpos_approved', kw)

    @http.route('/bancard/cancelled', type='json', auth='public', methods=['POST'], csrf=False)
    def vpos_bancard_cancelled(self, **kw):
        _logger.info('Respuesta de Bancard Cancelacion')
        return http.request.render('payment_vpos.vpos_cancelled', {})
