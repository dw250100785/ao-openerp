# -*- coding: utf-8 -*-
##############################################################################
#
#    Ursa Information Systems
#    Author: Adam O'Connor
#    Copyright (C) 2013 (<http://www.ursainfosystems.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _
	
# associate tracking numbers to delivery orders
class delivery_tracking_numbers(osv.osv):
    
    _name = "delivery.tracking.numbers"
    _description = "Delivery Tracking Numbers"
    _columns = {
        'delivery_id':fields.many2one('stock.picking.out', 'Delivery Order', required=False, ondelete='cascade', help=''),
        'tracking_no':fields.char('Tracking Number', size=64, required=False, help='Delivery Tracking Number'),
        'tracking_desc' : fields.char('Description', size=128, required=False, help='Delivery Tracking Number Description'),        
    }
    
delivery_tracking_numbers()    
    
# Modified to include multiple tracking numbers associated to one delivery
class do_tracking_add(osv.osv):

    _inherit = "delivery.tracking.numbers"

    def add_tracking_num(self, cr, uid, values, context=None):
        """  set delivery order id in the tracking number db table records on create
        """
        res = super(do_tracking_add, self).create(cr, uid, values, context=context)
        if 'tracking_nums' in values:
            for tracking_num in values['delivery_id']:
                track_id = super(do_tracking_add, self).write(cr, uid, res, values)
                #self.pool.get('stock.picking').write(cr, uid, values['delivery_id'], {'delivery_id':track_id})
        return res	

# Modified to include multiple tracking numbers associated to one delivery
class stock_picking(osv.osv):

    _inherit = "stock.picking"
    
    _columns = {
        'delivery_tracking_ids':fields.one2many('delivery.tracking.numbers', 'delivery_id', 'Tracking Numbers', states={'draft': [('readonly', False)]}),
    }
    
    def create(self, cr, uid, values, context=None):
        """  set delivery order id in the tracking number db table records on create
        """
        res = super(stock_picking, self).create(cr, uid, values, context=context)
        if 'delivery_tracking_ids' in values:
            for delivery_tracking_ids in values['delivery_tracking_ids']:
                self.pool.get('delivery.tracking.numbers').write(cr, uid, tracking_num_ids[1], {'delivery_id':res})
        return res
    
    def write(self, cr, uid, ids, values, context=None):
        """  set delivery order id in the tracking number db table records on create
        """
        if 'delivery_tracking_ids' in values:
            for delivery_tracking_ids in values['delivery_tracking_ids']:
                for id in ids:
                    if delivery_tracking_ids[2]:
                        delivery_tracking_ids[2]['delivery_id']=id
                        
        retval = super(stock_picking, self).write(cr, uid, ids, values, context=context)        
            
        return retval


# Modified to include multiple tracking numbers associated to one delivery
class stock_picking_out(osv.osv):

    _inherit = "stock.picking.out"
	
    _columns = {
        'delivery_tracking_ids':fields.one2many('delivery.tracking.numbers', 'delivery_id', 'Tracking Numbers', states={'draft': [('readonly', False)]}),
    }
    
    def create(self, cr, uid, values, context=None):
        """  set delivery order id in the tracking number db table records on create
        """
        res = super(stock_picking, self).create(cr, uid, values, context=context)
        if 'delivery_tracking_ids' in values:
            for delivery_tracking_ids in values['delivery_tracking_ids']:
                self.pool.get('delivery.tracking.numbers').write(cr, uid, tracking_num_ids[1], {'delivery_id':res})
        return res
    
    def write(self, cr, uid, ids, values, context=None):
        """  set delivery order id in the tracking number db table records on create
        """
        if 'delivery_tracking_ids' in values:
            for delivery_tracking_ids in values['delivery_tracking_ids']:
                for id in ids:
                    if delivery_tracking_ids[2]:
                        delivery_tracking_ids[2]['delivery_id']=id
                        
        retval = super(stock_picking_out, self).write(cr, uid, ids, values, context=context)        
            
        return retval

