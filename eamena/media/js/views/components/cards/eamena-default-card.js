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

        if(this.form)
        {
            for(i = 0; i < this.form.addableCards().length; i++)
            {
                self.data.push(ko.observable());
            }
        }

        this.saveValue = function(arg)
        {
            var index = arg();
            var savevalue = this.data()[index]();
            var atile = this.card.tiles()[0];
            // At this point, if atile is undefined, we need to create it.
            if(atile == null)
            {
                var topcard = this.card; // Explicitly set this here so the callback can access it
                self.tile.save(null, function(tileData) {

                    var newcard = topcard.tiles()[0].cards[index];
                    var newtile = newcard.getNewTile();
                    var keys = Object.keys(newtile.data);
                    for(i = 0; i < keys.length; i++)
                    {
                        if(keys[i].startsWith('_')) { continue; }
                        if(typeof newtile.data[keys[i]] === "function")
                        {
                            newtile.data[keys[i]](savevalue); // If this is an observable already, it'll be a function
                        } else {
                            newtile.data[keys[i]] = savevalue; // It's not an observable, so just set it.
                        }
                    }
                    newtile.save(null, function(created){ newcard.parent.selected(true); });
		});
            } else {

                var newcard = this.card.tiles()[0].cards[index];
                var newtile = newcard.getNewTile();
                var keys = Object.keys(newtile.data);
                for(i = 0; i < keys.length; i++)
                {
                    if(keys[i].startsWith('_')) { continue; }
                    if(typeof newtile.data[keys[i]] === "function")
                    {
                        newtile.data[keys[i]](savevalue); // If this is an observable already, it'll be a function
                    } else {
                        newtile.data[keys[i]] = savevalue; // It's not an observable, so just set it.
                    }
                }

                newtile.save(null, function(created){ newcard.parent.selected(true); });
            }
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
