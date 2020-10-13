function createPickr(idName) {
  const idEle = document.getElementById(idName)
  const pickr = Pickr.create({
    el: '#' + idName,
    theme: 'nano', // or 'monolith', or 'nano'

    default: idEle.style.backgroundColor,
    useAsButton: true,
    // comparison: false,
    defaultRepresentation: 'RGBA',

    swatches: [
      'rgba(244, 67, 54, 1)',
      'rgba(233, 30, 99, 0.95)',
      'rgba(156, 39, 176, 0.9)',
      'rgba(103, 58, 183, 0.85)',
      'rgba(63, 81, 181, 0.8)',
      'rgba(33, 150, 243, 0.75)',
      'rgba(3, 169, 244, 0.7)',
      'rgba(0, 188, 212, 0.7)',
      'rgba(0, 150, 136, 0.75)',
      'rgba(76, 175, 80, 0.8)',
      'rgba(139, 195, 74, 0.85)',
      'rgba(205, 220, 57, 0.9)',
      'rgba(255, 235, 59, 0.95)',
      'rgba(255, 193, 7, 1)'
    ],

    components: {

      // Main components
      preview: true,
      opacity: true,
      hue: true,

      // Input / output Options
      interaction: {
        hex: false,
        rgba: false,
        hsla: false,
        hsva: false,
        cmyk: false,
        input: true,
        clear: true,
        save: true
      },
    }
  }).on('save', color => {
    const selectColor = color.toRGBA().toString(1);
    idEle.style.backgroundColor = selectColor;
    document.getElementById(idName + '-code').value = selectColor;
    pickr.hide();
  }).on('cancel', color => {
    pickr.hide();
  });
}

function checkAndCreate(idName) {
  if (document.getElementById(idName)) {
    createPickr(idName);
  }
}
