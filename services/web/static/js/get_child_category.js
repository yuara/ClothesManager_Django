function createDropDown(getChildCateURL, parentCategory, childCategory) {
  const changeCategory = (select) => {
    // Empty choices of child categories
    childCategory.children().remove();

    $.ajax({
      url: getChildCateURL,
      type: 'GET',
      data: {
        'pk': parentCategory.val()
      }
    }).done(response => {
      // Create and add the choices of the child categories
      for (const category of response.categoryList) {
        const option = $('<option>');
        option.val(category['pk']);
        option.text(category['name']);
        childCategory.append(option);
      }

      // Choose the category if picked
      if (select !== undefined) {
        childCategory.val(select);
      }

    });
  };

  parentCategory.on('change', () => {
    changeCategory();
  });

  // If reloaded when something happens, create child categories
  if (parentCategory.val()) {
    const selectedCategory = childCategory.val();
    changeCategory(selectedCategory);
  }
}
