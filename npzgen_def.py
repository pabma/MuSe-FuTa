from skimage import measure
from stl import mesh
import gc
import numpy as np

def pointsgen(image_Z):
    # Use marching cubes to obtain the surface mesh
    verts, faces, normals, values = measure.marching_cubes(image_Z[0,:,:,:],0.5,step_size=1.0)
    # Create the mesh
    data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
    my_mesh = mesh.Mesh(data, remove_empty_areas=False)
    # Populate the mesh data
    my_mesh.vectors = verts[faces]
    #my_mesh.save('my_mesh.stl')
    #A = mesh.Mesh.from_file("my_mesh.stl")
    #POINTS = np.mean(A.vectors,axis=1)
    POINTS = np.mean(my_mesh.vectors,axis=1) #POINTS over the surface

    return POINTS

    gc.collect()

gc.collect()