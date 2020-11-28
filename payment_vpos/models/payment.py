# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import uuid

from hashlib import md5
from werkzeug import urls, utils
import requests
import pprint
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare


_logger = logging.getLogger(__name__)


class PaymentAcquirerVPos(models.Model):
    _inherit = 'payment.acquirer'

    amount = fields.Float()

    provider = fields.Selection(
        selection_add=[('vpos', 'vPOS')],
        ondelete={'vpos': 'set default'}
    )
    vpos_public_key = fields.Char(
        string="vPOS Public Key",
        required_if_provider='vpos',
        groups='base.group_user'
    )
    vpos_private_key = fields.Char(
        string="vPOS Private Key",
        required_if_provider='vpos',
        groups='base.group_user'
    )

    def _get_vpos_answ(self, environment):
        """ devuelve la respuesta de bancard"""

        env_staging = "https://vpos.infonet.com.py:8888"
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        private_key = self.vpos_private_key
        shop_process_id = self.env['ir.sequence'].next_by_code('process_id_sequence')
        amount = '{0:.2f}'.format(self.amount)
        currency = "PYG"
        _logger.info('Procesando pago id=%s' % shop_process_id)

        token = md5(private_key.encode('utf-8') +
                    shop_process_id.encode('utf-8') +
                    amount.encode('utf-8') +
                    currency.encode('utf-8'))

        data = {
            "public_key": self.vpos_public_key,
            "operation": {
                "token": token.hexdigest(),
                "shop_process_id": shop_process_id,
                "currency": currency,
                "amount": amount,
                "additional_data": "",
                "description": "Testeando el pago desde odoo",
                "return_url": "%s/bancard/return_url" % base_url,
                "cancel_url": "%s/bancard/cancelled" % base_url
            }
        }

        _logger.info('Data sent to bancard \n%s', pprint.pformat(data))

        answ = requests.post(url="%s/vpos/api/0.3/single_buy" % env_staging, json=data)
        return answ

    def vpos_form_generate_values(self, values):
        """ que le pasa el amount por variable global
        """
        self.amount = values['amount']
        return dict()

    def vpos_get_form_action_url(self):
        """ ############################################################################
            Metodo que devuelve la url del controller que va a lanzar el formulario para
            cargar la tarjeta.
            Se le pasa como parametro la url de bancard
        """
        env_staging = "https://vpos.infonet.com.py:8888"
        env_prod = "https://vpos.infonet.com.py"

        self.ensure_one()
        environment = 'prod' if self.state == 'enabled' else 'test'
        answ = self._get_vpos_answ(environment)
        if answ.ok:
            json = answ.json()
            process_id = json.get('process_id')
            bancard_url = '%s/checkout/new?process_id=%s' % (env_staging, process_id)
            return '/bancard?url=%s' % bancard_url
        else:
            return '/bancard/error'
