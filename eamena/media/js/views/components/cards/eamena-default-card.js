define([
    'knockout',
    'viewmodels/card-component'
], function(ko, CardComponentViewModel) {

    var viewModel = function(params) {
        var self = this;
        this.card = params.card;
        this.form = params.form;
        this.expanded = ko.observable(true);
        this.data = ko.observableArray();

	for(i = 0; i < 100; i++) { this.data.push(ko.observable('')); } // hacky

        this.saveValue = function(arg)
        {
            var index = arg();
            var tiles = this.card.tiles()[0].cards[index].tiles();


            var newtile = this.card.tiles()[0].cards[index].getNewTile();
            var dataid = newtile.nodegroup_id;
            newtile.data[dataid] = this.data()[index]();
            newtile.save();
        };

        params.configKeys = ['selectSource', 'selectSourceLayer'];

        CardComponentViewModel.apply(this, [params]);
    };
    return ko.components.register('eamena-default-card', {
        viewModel: viewModel,
        template: {
            require: 'text!templates/views/components/cards/eamena-default-card.htm'
        }
    });
});