jQuery.fn.tabs = function () {
  function parseId(url) {
    return /#([a-z][\w.:-]*)$/i.exec(url)[1];
  }

  var id = window.location.hash.substr(1);

  return this.each(function () {
    var previousSelected = null,
        previousPart = null;

    $(this).find("li a").each(function () {
      var editPart = $("#" + parseId(this.href));

      if (editPart.length) {
        editPart.hide();

        $(this).click(function () {
          if (previousPart) {
            previousPart.hide();
          }
          if (previousSelected) {
            previousSelected.removeClass("selected");
          }

          previousPart = editPart.show();
          previousSelected = $(this).addClass("selected");

          return false;
        });

        if ($(this).hasClass("selected")) {
          $(this).click();
        }
      }
    });

    $(this).find("li a[href='#" + id + "']").click();

    if (previousPart == null) {
      $($(this).find("li a")[0]).click();
    }
  });
};
