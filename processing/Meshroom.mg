{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "0.7.1",
        "fileVersion": "1.1",
        "nodesVersions": {
            "MeshFiltering": "3.0",
            "CameraInit": "4.0",
            "MultiviewStereoCL": "1.0",
            "StructureFromMotionCL": "1.0",
            "TexturingCL": "1.0"
        }
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                0,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 0,
                "split": 1
            },
            "uids": {
                "0": "f9436e97e444fa71a05aa5cf7639b206df8ba282"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "viewpoints": [],
                "intrinsics": [],
                "sensorDatabase": "cameraSensors.db",
                "defaultFieldOfView": 45.0,
                "groupCameraFallback": "folder",
                "allowedCameraModels": [
                    "pinhole",
                    "radial1",
                    "radial3",
                    "brown",
                    "fisheye4",
                    "fisheye1"
                ],
                "useInternalWhiteBalance": true,
                "viewIdMethod": "metadata",
                "viewIdRegex": ".*?(\\d+)",
                "verboseLevel": "info"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/cameraInit.sfm"
            }
        },
        "StructureFromMotionCL_1": {
            "nodeType": "StructureFromMotionCL",
            "position": [
                200,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 0,
                "split": 1
            },
            "uids": {
                "0": "c7cd0a37febf11a20edff8b6911874d9b43d91b0"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{CameraInit_1.output}",
                "maxImageSize": 2400,
                "DomainSizePooling": true,
                "GuidedMatching": true,
                "bundleAdjustmentQuality": "default",
                "maxNumThreads": 16,
                "cpuOnly": false,
                "OpenCLDevices": true,
                "Devices": [
                    "0:0_AMD_Accelerated_Parallel_Processing_gfx1012"
                ]
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/sfm.abc",
                "outputViewsAndPoses": "{cache}/{nodeType}/{uid0}/cameras.sfm",
                "extraInfoFolder": "{cache}/{nodeType}/{uid0}/"
            }
        },
        "MultiviewStereoCL_1": {
            "nodeType": "MultiviewStereoCL",
            "position": [
                400,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 0,
                "split": 1
            },
            "uids": {
                "0": "15b5b1df586045008cca26a8a558bd6d790b3e08"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "input": "{StructureFromMotionCL_1.output}",
                "sfmFolder": "{StructureFromMotionCL_1.extraInfoFolder}",
                "meshingMethod": "delaunay",
                "poissonDepth": 13,
                "maxImageSize": 2400,
                "windowRadius": 5,
                "maxSourceImages": 10,
                "OpenCLDevices": "{StructureFromMotionCL_1.OpenCLDevices}",
                "Devices": "{StructureFromMotionCL_1.Devices}",
                "computeVisibility": false
            },
            "outputs": {
                "outputMesh": "{cache}/{nodeType}/{uid0}/mesh.obj",
                "output": "{cache}/{nodeType}/{uid0}/densePointCloud.abc",
                "outputFolder": "{cache}/{nodeType}/{uid0}/"
            }
        },
        "MeshFiltering_1": {
            "nodeType": "MeshFiltering",
            "position": [
                600,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 1,
                "split": 1
            },
            "uids": {
                "0": "2cedf90275462006625178787d37e06d4aa921dd"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "inputMesh": "{MultiviewStereoCL_1.outputMesh}",
                "keepLargestMeshOnly": false,
                "smoothingSubset": "all",
                "smoothingBoundariesNeighbours": 0,
                "smoothingIterations": 0,
                "smoothingLambda": 1.0,
                "filteringSubset": "all",
                "filteringIterations": 1,
                "filterLargeTrianglesFactor": 60.0,
                "filterTrianglesRatio": 0.0,
                "verboseLevel": "info"
            },
            "outputs": {
                "outputMesh": "{cache}/{nodeType}/{uid0}/mesh.obj"
            }
        },
        "TexturingCL_1": {
            "nodeType": "TexturingCL",
            "position": [
                800,
                0
            ],
            "parallelization": {
                "blockSize": 0,
                "size": 0,
                "split": 1
            },
            "uids": {
                "0": "0c7eef0225afcc599be023b506f94cc0fda32031"
            },
            "internalFolder": "{cache}/{nodeType}/{uid0}/",
            "inputs": {
                "inputMesh": "{MeshFiltering_1.outputMesh}",
                "input": "{MultiviewStereoCL_1.outputFolder}"
            },
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/",
                "outputMesh": "{cache}/{nodeType}/{uid0}/texturedMesh.obj",
                "outputMaterial": "{cache}/{nodeType}/{uid0}/texturedMesh.mtl",
                "outputTextures": "{cache}/{nodeType}/{uid0}/texturedMesh_material*_map_Kd.png"
            }
        }
    }
}