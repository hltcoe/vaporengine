/*
 *
 */

var TermCloudItemModel = Backbone.Model.extend({
});

var TermCloudCollection = Backbone.Collection.extend({
  model: TermCloudItemModel,
  parse: function(data) {
    return data.terms;
  },
  url: function() {
    throw "You must override the Termcloud instance's 'url' property";
  },
});

var TermCloudItemView = Backbone.View.extend({
  tagName: 'span',
  className: 'wordcloud_token',

  render: function() {
    this.$el.attr('id', 'termcloud_item_' + this.model.attributes.term_id);

    // Add CSS classes for each audio_fragment_id
    var span_classes = [];
    for (var i = 0; i < this.model.attributes.audio_fragment_ids.length; i++) {
      span_classes.push("audio_fragment_span_" + this.model.attributes.audio_fragment_ids[i]);
    }
    this.$el.addClass(span_classes.join(" "));

    this.$el.text(termLabelText(this.model.attributes));

    return this;
  }
});

var TermCloud = Backbone.View.extend({
  el: '#termcloud',

  events: {
    'click .wordcloud_token': 'onTermClick'
  },
  onTermClick: function(event) {
    // Update active term.  There can be only one active term at a time
    this.$(".active_wordcloud_token").removeClass("active_wordcloud_token");
    $(event.currentTarget).addClass("active_wordcloud_token");

    // Retrieve the model associated with the ItemView that was
    // clicked on, using the strategy described in this blog post:
    //   https://lostechies.com/derickbailey/2011/10/11/backbone-js-getting-the-model-for-a-clicked-element/
    var cid = $(event.currentTarget).data('cid');
    var model = this.collection.get(cid);

    // Trigger custom event
    this.trigger('click_model', model);
  },

  initialize: function() {
    this.listenTo(this.collection, 'sync', this.render);
  },
  render: function() {
    var $list = this.$('div.termcloud_terms').empty();

    this.collection.each(function(model) {
      var item = new TermCloudItemView({model: model});
      var item_el = item.render().$el;

      // Save Backbone.js client id (http://backbonejs.org/#Model-cid)
      // as jQuery data attribute.  We can use the cid to retrieve a
      // model from a collection, using:
      //   collection.get(cid)
      item_el.data('cid', model.cid);

      // Adjust size of word based on size_key
      item_el.css('font-size', Math.sqrt(model.attributes[this.size_key]) + 'em');

      // Add tooltip
      var tooltip_text = "";
      for (var i in this.sort_keys) {
        tooltip_text += this.sort_keys[i].key_description + ": " + model.attributes[this.sort_keys[i].key_name] + "\n";
      }
      item_el
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', tooltip_text)
        .tooltip();

      $list.append(item_el);
    }, this);

    return this;
  },

  size_key: '',
  size_keys: [],
  sort_key: '',
  sort_keys: []
});


function termLabelText(term) {
  if (term.label) {
    return term.label;
  }
  else {
    return "T" + term.zr_term_index;
  }
}
