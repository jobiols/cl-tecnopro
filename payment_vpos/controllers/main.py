# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class VPosController(http.Controller):

    @http.route('/bancard', type='http', auth='public', csrf=False, website=True)
    def vpos_bancard(self, **kw):
        _logger.info('Enviando peticion a bancard')

        # le cambio el render por un redirect.
        # return http.request.render('payment_vpos.vpos_iframe', {
        #         "iframe_url": kw.get('url')
        #     })
        # dice que no tiene redirect, le agrego website=true
        return http.request.redirect(kw.get('url'))

    @http.route('/bancard/error', type='http', auth='public', csrf=False)
    def vpos_bancard_error(self, **kw):
        _logger.error('Error interno al procesar datos')
        return http.request.render('payment_vpos.vpos_error', {})

#   @http.route('/bancard/return_url', type='json', auth='public', methods=['POST'], csrf=False, website=True)
# cambio type=json por http | Da una excepcion dice que tiene que ser tipo json
    @http.route('/bancard/return_url', type='json', auth='public', methods=['POST'], csrf=False, website=True)
    def vpos_bancard_return_url(self, **kw):
        _logger.info('Recibiendo respuesta de Bancard ------------------------------- ')

        # obtener los datos enviados por bancard despues de la transaccion
        data = request.jsonrequest
        _logger.info('\n%s',  pprint.pformat(data))

        # esto da este error 'JsonRequest' object has no attribute 'render'
        #ans = http.request.render('payment_vpos.show_answer', {})
        #_logger.info('Redirected response %s', ans.response)
        #werkzeug.request.render('payment_vpos.show_answer', {})

        #acquirer = request.env['payment.acquirer'].browse(14)

        #reference = '/bancard/show_answer'
        #amount = float(data['operation']['amount'])
        #currency_id = False
        #values = data
        #acquirer.sudo().render(reference, amount, currency_id, partner_id=False, values=None)
        # el objeto ir.ui.view no tiene render_template

        #return request.redirect('/bancard/show_answer') no hace nada....
        # intento renderizar en lugar de redireccionar. no anda
        #return request.render('payment_vpos.vpos_cancelled', {})

        # a ver esta respuesta loca... no anda...
        #return '/bancard/cancelled'

#       esto no hace nada
#        template = request.env.ref('payment_vpos.show_answer')
#        return template._render(data)
        # pongo el redirect pero con methods POST
        #ret = request.redirect('/bancard/show_answer', code=301)
        #_logger.info('Respuesta del redirect %s', str(ret))
        #return ret
#       codigo copiado de google no anda.
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': '/bancard/show_answer',
        #     'target': 'self'
        # }

        # https://www.odoo.com/fr_FR/forum/aide-1/how-to-call-odoo-data-from-json-controller-175523
        # return request.env['ir.ui.view']._render_template('payment_vpos.show_answer', data)

        # request.env['payment.transaction'].sudo().form_feedback(
        #     data, 'vpos')
        # return werkzeug.utils.redirect("/bancard/show_answer")

        # return request._render('payment_vpos.show_answer', data)
        # return http.request.env['ir.ui.view'].render_template("payment_vpos.show_answer", {'data': data})
        headers=[('Content-Type', 'text/html; charset=utf-8')]
        response = response(headers=headers)
        response.set_default('payment_vpos.show_answer')
        return response.render({'data': data})

    @http.route('/bancard/show_answer', auth='public', website=True)
    def vpos_show_answer(self, **kw):
        _logger.info('answer response %s', str(kw))
        return http.request.render('payment_vpos.vpos_approved', kw)

    @http.route('/bancard/cancelled', type='http', auth='public', csrf=False)
    def vpos_bancard_cancelled(self, **kw):
        _logger.info('Respuesta de Bancard Cancelacion')
        return http.request.render('payment_vpos.vpos_cancelled', {})


    # esta redireccion funciona testeando -> bancard/error
    @http.route('/testeando', type='http', auth='public', website=True, csrf=False)
    def vpos_testeando(self, **kw):
        _logger.info('Testeando ********************')
        return request.redirect('/bancard/error')
