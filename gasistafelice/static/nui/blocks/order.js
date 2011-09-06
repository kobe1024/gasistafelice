
jQuery.UIBlockOrderReport = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("order", "table");
        this.active_view = "edit_multiple";
        this.default_view = this.active_view;
        this.submit_name = "Metti nel paniere";
    },

    action_handler : function(action_el) {
        if (action_el.attr('name') == 'createpdf') {
            window.location = action_el.attr('url');
        } else {
            return this._super(action_el);
        }
    },

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'bPaginate': false, 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aaSorting": [[5,"dsc"]],
                "aoColumns": [
                    null,
                    null,
                    { "bSortable": "false" },
                    { "bSortable": "false" },
                    { "bSortable": "false", 
                      "sType": "currency",
                      "fnRender": function (oObj) {
                                    return '&#8364; ' + oObj.aData[4];
                                  },
                    },
                    { "bSortable": "false",
                      "fnRender": function ( oObj ) {
                                    var step = $(oObj.aData[5]).attr('step');
                                    var min =  $(oObj.aData[5]).attr('minimum_amount');
                                    var rv = '<a href="#" onclick="var el = $(this).next(\'input\'); \
                                                var prev_row_total = parseInt(el.val())*' + parseFloat(oObj.aData[4].substr(8).replace(',','.')) + '; \
                                                var n = parseInt(el.val()); n == ' + min + '? el.val(0) : (n > ' + min +' ? \
                                                    el.val(n-' + step +') : 0); \
                                                var next_td = $(this).parent(\'td\').next(); \
                                                var row_total = parseInt(el.val())*' + parseFloat(oObj.aData[4].substr(8).replace(',','.')) + '; \
                                                next_td.html(\'&#8364; \' + row_total); \
                                                var total = parseFloat($(\'#total-order\').html().substr(2).replace(\',\',\'.\')) + row_total - prev_row_total; \
                                                $(\'#total-order\').html(\'&#8364; \' + total); \
                                                return false"><img src="/static/nui/img/remove.png">\
                                             </a>'; 
                                    rv += oObj.aData[5]; 
                                    rv += '<a href="#" onclick="var el = $(this).prev(\'input\'); \
                                            var prev_row_total = parseInt(el.val())*' + parseFloat(oObj.aData[4].substr(8).replace(',','.')) + '; \
                                            var n = parseInt(el.val()); el.val(n+' + step +'); \
                                            var next_td = $(this).parent(\'td\').next(); \
                                            var row_total = parseInt(el.val())*' + parseFloat(oObj.aData[4].substr(8).replace(',','.')) + '; \
                                            next_td.html(\'&#8364; \' + row_total); \
                                            var total = parseFloat($(\'#total-order\').html().substr(2).replace(\',\',\'.\')) + row_total - prev_row_total; \
                                            $(\'#total-order\').html(\'&#8364; \' + total); \
                                            return false"><img src="/static/nui/img/add.png">\
                                          </a>';
                                    return rv
                                  },
                     },
                    { "sType": "currency" },
                ],
                "oLanguage": {
                    "sLengthMenu": gettext("Display _MENU_ records per page"),
                    "sZeroRecords": gettext("Nothing found"),
                    "sInfo": gettext("Showing _START_ to _END_ of _TOTAL_ records"),
                    "sInfoEmpty": gettext("Showing 0 to 0 of 0 records"),
                    "sInfoFiltered": gettext("(filtered from _MAX_ total records)")
                },
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {

                    var iTotal = 0;
                    for ( var i=0 ; i<aaData.length ; i++ )
                    {
                        iTotal += parseFloat(aaData[i][6].substr(8).replace(',','.'));
                    }
                    
                    /* Modify the footer row to match what we want */
                    var nCells = $(nRow).find('th');
                    $(nCells[1]).html('&#8364; ' + iTotal);

                    /* Modify Django management form info */
                    /* FIXME TODO AFTER 6 UGLY !!!*/
                    $('#' + block_obj.block_box_id + '-form-TOTAL_FORMS').val(iEnd-iStart);
                }
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["order"] = new jQuery.UIBlockOrderReport();

