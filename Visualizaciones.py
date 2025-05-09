'''
import trimesh
import matplotlib.pyplot as plt

# Ruta del archivo OBJ de ShapeNet
obj_path = "B:/MasterIE/datasets/ShapeNet/bottle/1c38ca26c65826804c35e2851444dc2f/models/model_normalized.obj"

# Cargar el modelo OBJ
mesh = trimesh.load(obj_path)

# Verificar si el modelo se cargó correctamente
if isinstance(mesh, trimesh.Trimesh):
    # Visualizar el modelo en 3D
    mesh.show()
else:
    print("El archivo cargado no es una malla 3D.")

'''
'''
import open3d as o3d

# Ruta del archivo PLY (cambia la ruta a tu archivo específico)
file_path = "B:/MasterIE/datasets/CO3D/bottle/34_1433_4388/pointcloud.ply"

# Cargar el archivo PLY
point_cloud = o3d.io.read_point_cloud(file_path)

# Visualizar la nube de puntos
o3d.visualization.draw_geometries([point_cloud])
'''

import vtk
import open3d as o3d
import numpy as np
import os

def read_vtk_as_mesh(file_path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()

    # Extraer vértices y caras
    vertices = np.array([polydata.GetPoint(i) for i in range(polydata.GetNumberOfPoints())])
    faces = np.array([
        [polydata.GetCell(i).GetPointId(j) for j in range(polydata.GetCell(i).GetNumberOfPoints())]
        for i in range(polydata.GetNumberOfCells())
    ])

    # Crear mesh en Open3D
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(faces)
    mesh.compute_vertex_normals()
    return mesh

def visualize_vtk_files(folder_path):
    vtk_files = [f for f in os.listdir(folder_path) if f.endswith('.vtk')]
    geometries = []

    for vtk_file in vtk_files:
        file_path = os.path.join(folder_path, vtk_file)
        try:
            mesh = read_vtk_as_mesh(file_path)
            if len(mesh.vertices) == 0:
                print(f"El archivo {vtk_file} no contiene geometría.")
                continue
            mesh.paint_uniform_color(np.random.rand(3))  # Color aleatorio para cada mesh
            geometries.append(mesh)
        except Exception as e:
            print(f"Error al cargar {vtk_file}: {e}")

    if geometries:
        o3d.visualization.draw_geometries(geometries)
    else:
        print("No se cargaron meshes.")

# Configura la ruta de tu carpeta con archivos VTK
folder_path = "B:/MasterIE/datasets/3D_IRCADb_01/3Dircadb1.6/MESHES_VTK"
visualize_vtk_files(folder_path)
