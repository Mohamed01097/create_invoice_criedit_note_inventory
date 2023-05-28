from odoo import fields,models,api,_

class Stock_Picking_CreateInvoice(models.Model):
    _inherit = 'stock.picking'

    def generate_invoice(self):
        invoice = self.fill_move_lines('out_invoice')
        invoice_before_confirmed = self.env['account.move'].create(invoice)
        invoice_after_confirmed = invoice_before_confirmed.action_post()
        return invoice_after_confirmed

    def generate_credit_note(self):
        cridit_note = self.fill_move_lines('out_refund')
        self.env['account.move'].create(cridit_note).action_post()

    def fill_move_lines(self,move_type):
        move_lines = []
        for line in self.move_ids_without_package:
            move_lines.append((0, 0, {
                'product_id': line.product_id,
                'quantity': line.product_uom_qty,
                'price_unit':line.product_id.lst_price,
                'tax_ids': [(6, 0, line.product_id.taxes_id.ids)]
            }))
        invoice_values = {
            'partner_id': self.partner_id.id,
            'move_type': move_type,
            'invoice_line_ids': move_lines
        }
        return invoice_values

