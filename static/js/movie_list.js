$(
  () => $('.show-image').popover(
    {
      html: true,
      trigger: 'hover',
      content: function() {
        return $('<img/>', {src: $(this).data('img'), class: 'fill-container'});
      }
    }
  )
);
