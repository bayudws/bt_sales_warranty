from odoo import api, fields, models, _
from datetime import datetime,timedelta,time

class Warranty(models.Model):
    
    _name = "warranty.details"
    _inherit = ['mail.thread']
    _description = "Warranty Record"
    
    @api.multi
    def count_service(self):
        count = self.env['service.details'].search_count([('warranty_id','=',self.id)])
        self.service_count = count
    
    @api.multi
    def count_campaign(self):
        count = self.env['campaign.details'].search_count([('warranty_id','=',self.id)])
        self.campaign_count = count

    name = fields.Char(string='Warranty NO',  copy=False,  index=True, default=lambda self: _('New'))
    internal_reference = fields.Text(string='Internal Reference')
    product_id = fields.Many2one('product.product',string='Product', track_visibility='onchange', related='sale_id.product_id')
    sno = fields.Char(string='Serial No',track_visibility='onchange')
    partner_id = fields.Many2one('res.partner',string='Customer', track_visibility='onchange', related='sale_id.partner_id')
    sale_id = fields.Many2one('sale.order', string='SO Reference')
    invoice_id = fields.Many2one('account.invoice',string='Invoice Reference')
    purchase_date = fields.Date(string='Delivery Date')
    warranty_end_date = fields.Date(string='Warranty End Date',track_visibility='onchange')
    qty_id = fields.Integer(string="Qty", required=True, default='1')
    state = fields.Selection([('inwarranty','In Warranty'),
                              ('toexpire','To Expire'),
                              ('expired','Expired')],string = "Status", default='inwarranty',track_visibility='onchange')
    not_interested = fields.Boolean(string="not interested",track_visibility='onchange')
    won_campaign = fields.Boolean(string = "won campaign",track_visibility='onchange')
    new_sales_id = fields.Many2one('sale.order',string='New sales reference')
    new_invoice_id = fields.Many2one('account.invoice',string='New invoice reference')
    service_count = fields.Integer(string='Service Count', compute = count_service)
    campaign_count = fields.Integer(string='Campaign Count', compute = count_campaign)
    responsible_id = fields.Many2one(comodel_name="res.users", 
        string="Responsible", required=True)
    sparepart_ids = fields.One2many(comodel_name="warranty.sparepart", 
        string="Component",
        inverse_name="warranty_id")
    pasang_id = fields.Char(string='Location',track_visibility='onchange')
    res_company = fields.Many2one('res.company',string='New sales reference')
    
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('warranty.details') 
        values['name'] = seq
        result = super(Warranty,self).create(values)
        return result 
    
    @api.multi
    def action_endcampaigns(self,vals):
        for campaign in self:
            campaign.not_interested = True

    @api.multi
    def action_woncampaigns(self,vals):
        for campaign in self:
            campaign.won_campaign = True
        
    @api.multi
    def action_warranty_services(self):
        services = self.env['service.details'].search([('warranty_id','=',self.id)])
        action = self.env.ref('bt_sales_warranty.sales_service_details_action').read()[0]
        action['context'] = {'default_warranty_id':self.id}
        if len(services) > 1:
            action['domain'] = [('id', 'in', services.ids)]
        elif len(services) == 1:
            action['views'] = [(self.env.ref('bt_sales_warranty.sales_service_details_form').id, 'form')]
            action['res_id'] = services.ids[0]  
        else:
            action['domain'] = [('id', 'in', services.ids)]
        return action
    
    @api.multi
    def action_warranty_campaign(self):
        campaign = self.env['campaign.details'].search([('warranty_id','=',self.id)])
        action = self.env.ref('bt_sales_warranty.sales_campaign_details_action').read()[0]
        action['context'] = {'default_warranty_id':self.id}
        if len(campaign) > 1:
            action['domain'] = [('id', 'in', campaign.ids)]
        elif len(campaign) == 1:
            action['views'] = [(self.env.ref('bt_sales_warranty.sales_campaign_details_form').id, 'form')]
            action['res_id'] = campaign.ids[0] 
        else:
            action['domain'] = [('id', 'in', campaign.ids)]
        return action

    @api.model
    def cron_warranty_expire(self):
        date_eval =  datetime.now()+timedelta(days=30)
        date_eval_str = date_eval.strftime('%Y-%m-%d')
        warranty_records = self.env['warranty.details'].search([('warranty_end_date','<=',date_eval_str),
                                                                ('state','=','inwarranty')])
        print '?????????warranty_records??????????',warranty_records
        for val in warranty_records:                        
            val.state = 'toexpire'
     
    @api.model
    def cron_warranty_expired(self):
        date_eval =  datetime.now()
        date_eval_str = date_eval.strftime('%Y-%m-%d')
        warranty_records = self.env['warranty.details'].search([('warranty_end_date','<=',date_eval_str)])
        print '==========warranty_records_expired==========', warranty_records
        for val in warranty_records:                        
            val.state = 'expired'        
        
# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:        
