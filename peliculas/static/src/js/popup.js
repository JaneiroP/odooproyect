odoo.define('odoo example',function(require){
  'use strict'

  console.log('Popup')
  var FormController = require('web.FormController');

  var ExtendFormController = FormController.include({
     saveRecord: function(){
       console.log('saveRecord')
       var res = this.super.apply(this,arguments);
       this.do_notify('Success', 'Record saved');
       return res;
     }
  })
})