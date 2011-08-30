
jQuery.UIBlockGASStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("gasstocks", "table");
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.dataSource + "?render_as=table",
                "aoColumns": [
                    null,
                    null,
                    null,
                    { "sType": "currency" },
                    null
                ]
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["gasstocks"] = new jQuery.UIBlockGASStockList();
