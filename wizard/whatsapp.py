from odoo import models, api, fields


class WhatsappSendMessage(models.TransientModel):
    
    _name = 'whatsapp.message.wizard'

    warranty_id = fields.Many2one('warranty.details',string='Warranty',related='')
    partner_id = fields.Many2one('res.partner',string='Customer', related='warranty_id.partner_id')
    # user_id = fields.Many2one('res.partner', string="Recipient")
    mobile = fields.Char(related='partner_id.mobile', required=True)
    complaint_note = fields.Text(string='Description',track_visibility='onchange')
    message = fields.Text(string="message", required=True)

    def send_message(self):
        if self.message and self.mobile:
            message_string = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone="+self.partner_id.mobile+"&text=" + message_string,
                'target': 'new',
                'res_id': self.id,
            }