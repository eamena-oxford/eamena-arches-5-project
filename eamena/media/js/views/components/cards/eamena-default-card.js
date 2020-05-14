define([
    'knockout',
    'viewmodels/card-component'
], function(ko, CardComponentViewModel) {

    var viewModel = function(params) {
        var self = this;

        this.state = params.state || 'form';
        this.preview = params.preview;
        this.loading = params.loading || ko.observable(false);
        this.provisionalTileViewModel = params.provisionalTileViewModel;

        this.card = params.card;
        this.form = params.form;
        this.expanded = ko.observable(true);
        this.values = ko.observableArray();

        // We check for the addableCards method here because it only exists in resource edit mode.
        // If we let the following for loop run unchecked while in (for example) card designer mode,
        // this function will stop mid-way through, causing all sorts of horrible HTML errors during
        // rendering.
        if(this.form && (this.state === 'form') && this.form.addableCards)
        {
            // This loop simply fills the 'values' array with enough observable values for the number
            // of widgets we're going to render.
            for(i = 0; i <= this.form.addableCards().length; i++)
            {
                self.values.push(ko.observable());
            }
        }

        this.saveValue = function(arg)
        {
            var index = arg();
            var savevalue = this.values()[index]();
            var atile = this.card.tiles()[0];
            // At this point, if atile is undefined, we need to create it. There is almost certainly a more
            // efficient way of doing this, but this works well for now.
            if(atile == null)
            {
                // This code block runs if there are no nodes created
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
                // This code block runs if there is a node, and we are just adding a value to it
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
