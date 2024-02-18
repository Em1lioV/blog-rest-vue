export default function objectToFormData(obj, cfg = {}, fd = new FormData(), pre = '') {
  const {
    indices = false,
    nullsAsUndefineds = false,
    booleansAsIntegers = false,
    allowEmptyArrays = false,
    noAttributesWithArrayNotation = false,
    noFilesWithArrayNotation = false,
    dotsForObjectNotation = false
  } = cfg;

  const isReactNative = typeof fd.getParts === 'function';

  function isObject(value) {
    return value === Object(value);
  }

  if (obj === undefined || (obj === null && !nullsAsUndefineds)) return fd;
  if (typeof obj === 'boolean') {
    fd.append(pre, booleansAsIntegers ? (obj ? 1 : 0) : obj);
  } else if (Array.isArray(obj)) {
    if (obj.length) {
      obj.forEach((value, index) => {
        let key = pre + (indices ? `[${index}]` : '[]');

        if (noAttributesWithArrayNotation || (noFilesWithArrayNotation && isFile(value, isReactNative))) {
          key = pre;
        }

        objectToFormData(value, cfg, fd, key); // Llamada recursiva a objectToFormData
      });
    } else if (allowEmptyArrays) {
      fd.append(noAttributesWithArrayNotation ? pre : pre + '[]', '');
    }
  } else if (obj instanceof Date) {
    fd.append(pre, obj.toISOString());
  } else if (typeof obj === 'object') {
    Object.entries(obj).forEach(([prop, value]) => {
      if (value === undefined || value === null || value === '') {
        // Omitir valores indefinidos, nulos o vacíos
        return;
      }

      const key = pre ? (dotsForObjectNotation ? `${pre}.${prop}` : `${pre}[${prop}]`) : prop;

      if (isObject(value) && ('key' in value || 'id' in value || 'pk' in value)) {
        fd.append(key, value.key || value.id || value.pk);
      } else if (isObject(value)) {
        objectToFormData(value, cfg, fd, key); // Llamada recursiva a objectToFormData
      } else {
        fd.append(key, value);
      }
    });
  } else {
    fd.append(pre, obj);
  }

  return fd;
}
