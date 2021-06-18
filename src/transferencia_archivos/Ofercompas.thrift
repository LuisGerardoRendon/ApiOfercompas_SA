namespace py OfercompasArchivos

typedef i32 int

struct Imagen {
    1: binary archivo,
    2: string ruta
}

exception ExcepcionArchivo{
    1: int codigoError,
    2: string descripcion
}

service ServicioDeAlmacenamiento{
    int guardarArchivo(1:Imagen imagen) throws (1: ExcepcionArchivo excepcion),
    list<binary> obtenerArchivos(1: string ruta) throws (1: ExcepcionArchivo excepcion),
    int eliminarArchivo(1: string ruta) throws (1: ExcepcionArchivo excepcion)
}