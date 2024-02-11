export const getValidationError = (error) => {
    const { response } = error;
    const statusCode = response ? response.status : null;
    const errorData = response ? response.data : null;

    const statusMatcher = {
        400: 'La solicitud no pudo ser procesada debido a datos incorrectos. Por favor, revisa los datos e inténtalo de nuevo.',
        401: 'No estás autorizado para acceder a esta página. Por favor, inicia sesión con una cuenta autorizada.',
        403: 'No tienes permiso para acceder a esta página. Por favor, ponte en contacto con el administrador del sistema.',
        500: 'Se ha producido un error en el servidor. Por favor, inténtalo de nuevo más tarde.',
    };

    const statusMessage = statusMatcher[statusCode];
    const errorMessage = statusMessage || 'Se ha producido un error. Por favor, inténtalo de nuevo más tarde.';

    const validationErrors = errorData && errorData.errors ? {} : null;
    if (errorData && errorData.errors) {
        for (let field in errorData.errors) {
            validationErrors[field] = errorData.errors[field][0];
        }
    }

    // Aquí agregamos el detalle del error al objeto retornado
    const errorDetails = {
        status: statusCode,
        original: error,
        validation: validationErrors || null,
        message: errorMessage,
        detail: errorData ? errorData.detail : null
    };

    return errorDetails;
};

