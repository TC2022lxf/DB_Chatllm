## 第 2 章安装与测试

### 2\.1 GROMACS 构建简介

以下说明适用于构建GROMACS 2019 看 最新安装说明↪https://manual\.gromacs\.org/documentation/current/install\-guide/index\.html。

#### 2\.1\.1 快速安装

1\.获取最新版本的C/C\+\+编译器。

2\.检查是否安装了CMake 3\.4\.3或更高版本。

3\.下载最新版本的GROMACS压缩包，并解压。

4\.创建一个单独的构建目录并进入。

5\.以源代码路径为参数运行cmake

6\.运行make，make check和make install
''''
source GMXRC后即可使用GROMACS或者，依次执行下列命令（Linux下需要先切换为超级用户）：

tar xfz gromacs\-2019\.6\.tar\.gz  
cd gromacs\-2019\.  
mkdir build  
cd build  
cmake \.\. \-DGMX\_BUILD\_OWN\_FFTW=ON \-DREGRESSIONTEST\_DOWNLOAD=ON  
make  
make check  
sudo make install  
source /usr/local/gromacs/bin/GMXRC

##### 上面的命令会先下载并构建必需的FFT库，然后构建GROMACS。如果已经安装了FFTW，可以删除

cmake中的第二个参数。总的来说，采用这种方法构建的GROMACS运行正常，而且在运行cmake的  
（安装）机器上速度良好。在另外的机器上，它可能无法运行，或运行速度较慢。如果你想使GROMACS  
发挥硬件的最大性能，必须进一步阅读下面的内容。遗憾的是，硬件，库和编译器之间的相互影响会让  
安装变得更加复杂。

#### 2\.1\.2 集群上的快速安装

##### 在集群上，用户可能希望使用MPI跨多个节点运行GROMACS，在这种情况下可以先采用类似上面的

##### 方式进行一次安装，

对于 2019 版本,可以再使用MPI封装的编译器单独构建 mdrun ↪ ?? ，因为mdrun模拟引擎是GROMACS

唯一使用MPI的组件。如果使用默认的后缀，单独构建时只会安装单个二进制文件mdrun\_mpi。

对于 2023 版本,则可以启用\-DGMX\_MPI=on,这样安装的二进制和库会使用默认的\_mpi即 gmx\_mpi后

缀。因此，将它安装到与非MPI版本的同一位置不会导致混淆，也是常见的做法。

#### 2\.1\.3 典型安装

安装过程如上所述，后面还会提供更多详细信息。安装时你应该考虑使用以下 CMake 选项↪ 14 ，并将将

xxx替换为适当的值：

\-DCMAKE\_C\_COMPILER=xxx:要使用的C 99 编译器↪ 7 的名称（或环境变量CC）

\-DCMAKE\_CXX\_COMPILER=xxx:要使用的C\+\+ 17 编译器↪ 7 的名称（或环境变量CXX）

\-DGMX\_MPI=on:构建时启用 MPI 支持↪ 9

\-DGMX\_GPU=CUDA:构建时启用NVIDIA CUDA支持。

\-DGMX\_GPU=OPENCL:构建时启用 OpenCL↪https://www\.khronos\.org/opencl/ 支持。

\-DGMX\_GPU=SYCL 构建时启用 SYCL↪https://www\.khronos\.org/sycl/ 支持 \(默认使用 Intel oneAPI  
DPC\+\+↪https://www\.intel\.com/content/www/us/en/developer/tools/oneapi/dpc\-compiler\.html\)\.

\-DGMX\_SYCL\_HIPSYCL=on 构建时启用SYCL↪https://www\.khronos\.org/sycl/支持，使用hipSYCL↪https:  
//github\.com/illuhad/hipSYCL \(需要\-DGMX\_GPU=SYCL\)\.

\-DGMX\_SIMD=xxx:指定GROMACS运行节点的 SIMD 支持↪ 14 的级别

\-DGMX\_DOUBLE=on:构建双精度版本的GROMACS（较慢，通常不启用）

\-DCMAKE\_PREFIX\_PATH=xxx:为CMake添加非标准位置，以搜索库，头文件或程序↪ 16

\-DCMAKE\_INSTALL\_PREFIX=xxx: 将GROMACS安装到非标准位置↪ 14 （默认为 /usr/local/  
gromacs）

\-DBUILD\_SHARED\_LIBS=off:不构建共享库，用于静态链接↪ 21

\-DGMX\_FFT\_LIBRARY=xxx:选择 FFT 支持↪ 10 所用的库，fftw3，mkl或fftpack

\-DCMAKE\_BUILD\_TYPE=Debug:构建调试模式的GROMACS

#### 2\.1\.4 构建旧版本

旧版本GROMACS的安装说明见GROMACS 文档页面↪http://manual\.gromacs\.org/documentation。

### 2\.2 安装条件

#### 2\.2\.1 平台

GROMACS可以在许多操作系统和机器架构下进行编译，支持的操作系统包括Linux，macOS或  
Windows的任何发行版；支持的机器架构包括x86，AMD64/x86\-64，一些PowerPC（包括POWER9，  
ARM v8和RISC\-V）。

#### 2\.2\.2 编译器

##### GROMACS可以在具有ANSI C99和C\+\+17编译器及其标准C/C\+\+库的任何平台上进行编译。在

一个操作系统和体系架构上要达到良好性能，需要选择一个好的编译器。我们推荐gcc，因为它是自由  
程序，应用广泛并且经常能够提供最佳性能。

你应该尽量使用最新版本的编译器。由于编译时需要C\+\+17的完整支持，因此GROMACS团队支持  
的编译器的最低版本为

GNU \(gcc/libstdc\+\+\) 9

LLVM \(clang/libc\+\+\) 7

Microsoft \(MSVC\) 2019

其他编译器可能可行（Cray，Pathscale，老的clang），但性能不够好。我们建议不要使用PGI，因为其  
C\+\+性能非常差。

GROMACS不再支持经典的Intel编译器\(icc/icpc\)。使用来自oneAPI基于clang的Intel更新的编译  
器，或gcc。

不支持xlc编译器，并且尚未在POWER体系架构上编译GROMACS\-2023\.3\.6。我们建议使用GCC  
编译器，版本9\.x到11\.x。注意：GCC 12以及更新版本存在已知问题\.

除编译器本身之外，你可能还需要使用其他编译器工具链组件（例如汇编器或链接器）的最新版本，它  
们通常由OS发行版的binutils包提供。

对C\+\+17，需要编译器和C\+\+库都提供足够的支持。gcc和MSVC编译器都自带了标准库，无需进  
一步配置。如果供应商的编译器也能以编译选项来管理标准库，那就更好了。有关其他编译器的配置，  
见后面的说明。

在Linux上，clang编译器使用的C\+\+库通常是来自g\+\+的libstdc\+\+。对于GROMACS，我们要  
求编译器支持libstc\+\+ 7\.1或更高版本。如果一个编译器的默认标准库无法使用，可以选择特定的  
libstdc\+\+库，这时需要使用\-DGMX\_GPLUSPLUS\_PATH=/path/to/g\+\+提供g\+\+的路径\.注意,如果你后  
面还要构建依赖于GROMACS的进一步项目,你需要保证使用相同的编译器和libstc\+\+\.

要使用clang和llvm的libcxx标准库进行构建，请使用\-DCMAKE\_CXX\_FLAGS=\-stdlib=libc\+\+。

如果要在Mac OS X上运行，最好选择gcc编译器。MacPorts提供的Apple clang编译器可以工作,但  
不支持OpenMP,因此可能无法提供最佳性能\.

对于所有的非x86平台，最好的选择通常是使用gcc或者供应商默认或推荐的编译器，并检查后面的特  
殊说明。

要将更新版本的gcc添加到Linux操作系统，请参阅

- Ubuntu: Ubuntu工具链ppa页面↪https://launchpad\.net/~ubuntu\-toolchain\-r/\+archive/ubuntu/test
- RHEL/CentOS: EPEL页面↪https://fedoraproject\.org/wiki/EPEL 或RedHat开发者工具集

#### 2\.2\.3 使用并行选项进行编译

##### 为获得最佳性能，需要确定你要如何使用GROMACS，并检查你计划运行GROMACS的硬件。

OpenMP↪http://en\.wikipedia\.org/wiki/OpenMP 并行通常是GROMACS的一个优势，但对其支持通常内置于编  
译器中并会自动检测。

##### GPU 支持

GROMACS对使用CUDA的NVIDIA GPU支持良好。在Linux上，NVIDIA CUDA↪http://www\.nvidia\.  
com/object/cuda\_home\_new\.html工具包的最低版本为11\.0，强烈建议使用最新版本。NVIDIA GPU至少需要具  
有NVIDIA计算能力3\.5。强烈建议使用你所用硬件支持的最新CUDA版本和驱动程序，但要注意在旧  
硬件上较新的CUDA版本可能导致性能下降。虽然一些CUDA编译器（nvcc）可能无法正式将最新版  
本的gcc作为后端编译器，但我们仍然建议你至少使用足够新的gcc版本来获得对CPU的最佳SIMD  
支持，因为GROMACS总会在CPU上运行一些代码。使用与编译nvcc的C\+\+编译器相同的版本来  
编译GROMACS代码是最可靠的。

为了能够使用其他加速器，GROMACS还支持 OpenCL↪https://www\.khronos\.org/opencl/作为可移植的GPU  
后端。OpenCL的最低版本未知，并且只支持 64 位实现。当前的OpenCL实现推荐用于基于GCN  
的AMD GPU，在Linux上，我们建议使用ROCm运行时。Neo驱动程序支持Intel集成的GPU。  
NVIDIA GPU也支持OpenCL，但建议使用最新的NVIDIA驱动程序（包括NVIDIA OpenCL运行  
时）。还要注意，存在性能限制（这是NVIDIA OpenCL运行时所固有的）。OpenCL无法同时支持Intel  
和其他供应商的GPU。此外，需要 64 位OpenCL实现，因此OpenCL只受 64 位平台支持\.

请注意, OpenCL后端不支持以下GPU:

- NVIDIA Volta \(CC 7\.0,例如Tesla V100或GTX 1630\)或更新版本,
- AMD RDNA1/2/3 \(Navi 1/2X,3X,例如RX 5500或RX6900\)\.

自GROMACS 2021开始支持SYCL↪https://www\.khronos\.org/sycl/\.自GROMACS 2023年开始，SYCL↪https:  
//www\.khronos\.org/sycl/ 后端已经成熟到与CUDA后端功能接近，并且支持广泛的平台，在这两方面都  
比OpenCL↪https://www\.khronos\.org/opencl/ 后端更加通用（值得注意的例外是Apple Silicon GPU，它只受  
OpenCL支持）。然而，由于缺乏广泛的测试，SYCL↪https://www\.khronos\.org/sycl/还不能完全取代OpenCL↪https:  
//www\.khronos\.org/opencl/成为一个GPU可移植性后端。当前的SYCL实现可以使用针对Intel GPU的Intel  
oneAPI DPC\+\+↪https://www\.intel\.com/content/www/us/en/developer/tools/oneapi/dpc\-compiler\.html编译器进行编译，也可以  
使用针对AMD GPU（GFX9、CDNA 1/2和RDNA1/2/3）的hipSYCL↪https://github\.com/illuhad/hipSYCL编  
译器和ROCm运行时进行编译。也可以使用这些编译器支持的其他设备，但不建议。

无法在GROMACS的同一构建中配置多个GPU后端。

##### MPI 支持

##### GPU 感知的 MPI

##### GROMACS可以使用其内置的线程MPI在单个工作站的多个核心上并行运行。启用此功能不需要用户

##### 进行任何操作。

##### 如果你希望在一个网络中的多台计算机上并行运行GROMACS，则需要安装一个支持MPI 2\.0标准的

##### MPI库。这适用于自 2009 年以来发布的任何MPI库版本，但GROMACS团队推荐使用供应商提供的

库、OpenMPI↪http://www\.open\-mpi\.org 或 MPICH↪http://www\.mpich\.org的最新版本（以获得最佳性能）。

要使用MPI进行编译，请将编译器设置为常规（非MPI）编译器，并在cmake选项中添加\-DGMX\_\-  
MPI=on。也可以将编译器设置为MPI编译器的包装器，但既无必要也不推荐。

##### 支持

##### 在使用多个GPU的模拟中，支持GPU的MPI实现允许在不同的GPU内存空间之间直接进行通信，

##### 而无需通过CPU内存分流，这通常会带来更高的带宽和更低的通信延迟。对于此, GROMACS目前只

支持针对Nvidia GPU的CUDA构建,且使用”CUDA感知”的MPI库。更多细节，请参见 CUDA感  
知的MPI简介↪https://developer\.nvidia\.com/blog/introduction\-cuda\-aware\-mpi/。

要将CUDA感知MPI用于GPU直接通信，我们建议使用最新的OpenMPI版本（>=4\.1\.0）和  
最新的UCX版本（>=1\.10），因为GROMACS对CUDA感知支持的大部分内部测试都是使用  
这些版本进行的。要构建支持CUDA感知的OpenMPI,可以按照 这些OpenMPI构建说明↪https:

intel\.com/content/www/us/en/develop/documentation/mpi\-developer\-reference\-linux/top/environment\-variable\-reference/gpu\-support\.html GPU  
感知支持。

对于AMD GPU上的GPU感知MPI支持，几种支持UCX的MPI实现都可以工作，我们推荐使用最  
新的OpenMPI版本（>=4\.1\.4）和最新的UCX（>=1\.13），因为我们的大部分测试都是使用这些版本  
完成的。其他MPI实现,如Cray MPICH,也支持GPU感知，并与ROCm兼容。

使用GMX\_MPI=ON时，GROMACS在编译时会尝试自动检测底层MPI库对GPU的支持，并在检测到  
GPU支持时启用直接GPU通信。不过，在某些情况下，GROMACS可能无法检测到存在的GPU感  
知MPI支持，在这种情况下，可以在运行时通过设置环境变量GMX\_FORCE\_GPU\_AWARE\_MPI=1来手动  
启用（因为这种情况仍然缺乏实质性的测试，所以我们敦促用户将结果与使用默认构建选项所得的结果  
进行对照,//www\.open\-mpi\.org/faq/?category=buildcuda中的步骤。

要实现Intel GPU对GPU感知MPI的支持，请使用不早于2018\.8版本的Intel MPI。这样的版本  
可以从oneAPI SDK 2023\.0或更新版中找到。在运行时，必须使用LevelZero SYCL后端（通常设置  
环境变量 SYCL\_DEVICE\_FILTER=level\_zero:gpu就足够了），并在MPI运行时 选择使用↪https://www\.

##### 仔细检查其正确性，并报告任何问题）。

#####  

#### 2\.2\.4 CMake

GROMACS使用CMake构建系统进行构建，需要的版本至少为3\.18\.4。你可以使用cmake \-\-version  
来检查是否安装了CMake，以及安装的版本。如果你需要安装CMake，请首先检查所用平台的软件包  
管理系统是否提供了合适的版本，或者访问 CMake安装页面↪http://www\.cmake\.org/install/ 下载预编译的二  
进制文件，源代码和安装说明。GROMACS团队建议你尽可能安装最新版本的CMake。

#### 2\.2\.5 快速傅里叶变换库

##### GROMACS中的许多模拟都广泛使用快速傅里叶变换，因此始终需要一个软件库来执行这些变换。我们

建议使用 FFTW↪http://www\.fftw\.org（ 3 或更高版本）或Intel MKL↪https://software\.intel\.com/en\-us/intel\-mkl。可以  
使用cmake \-DGMX\_FFT\_LIBRARY=来选择库，其中 可选fftw3，mkl或 fftpack之  
一。FFTPACK与GROMACS一起发布，作为备用，如果不需要优先考虑模拟性能，可以使用它。如  
果选择MKL，GROMACS也会使用MKL的BLAS和LAPACK（参见线性代数库↪ 22 ）。一般来说，将  
MKL与GROMACS配合使用没有优势，而且FFTW通常更快。使用CUDA支持PME GPU卸载时，  
还需要一个基于GPU的FFT库。基于CUDA的GPU FFT库cuFFT是CUDA工具包的一部分（所  
有CUDA构建都需要），因此在使用CUDA GPU加速构建时不需要额外的软件组件。

##### 使用 FFTW

在你的平台上，或许可以使用软件包管理系统来安装 FFTW↪http://www\.fftw\.org，但这样安装可能存在兼容  
性问题以及显著的性能问题。特别是，GROMACS模拟通常以“混合”浮点精度运行，适合使用单精度  
的FFTW。默认的FFTW包通常是双精度的，并且在链接到GROMACS时可能没有使用好的FFTW  
编译器选项。因此，GROMACS团队建议

- 安装时允许GROMACS自动下载FFTW源代码并进行构建（使用 cmake\-DGMX\_Build\_Own\_\-  
FFTW=ON），或
- 自己从源代码构建FFTW。

如果你自己从源代码构建FFTW，请获取最新版本并遵循 FFTW安装指南↪http://www\.fftw\.org/doc/  
Installation\-and\-Customization\.html\#Installation\-and\-Customization。选择FFTW的精度（即单/浮点精度还是双精度），  
这要与以后GROMACS使用混合精度还是双精度保持一致。没有必要编译具有线程或MPI支持的  
FFTW，但那样做也没问题。在x86硬件上，对FFTW\-3\.3\.4及更早版本，同时使用\-\-enable\-sse  
和\-\-enable\-avx选项进行编译。从FFTW\-3\.3\.5开始，还应该添加\-\-enable\-avx2选项。在支持 512  
宽度AVX的Intel处理器上，包括KN1，还要添加\-\-enable\-avx512选项。FFTW会为所有不同的  
指令集创建一个带有代码集的臃肿库，并在运行时选择受支持的速度最快的那个。对于具有SIMD支持  
的ARM架构和IBM Power8及更高版本，你肯定需要3\.3\.5或更高版本，并分别使用\-\-enable\-neon  
和\-\-enable\-vsx进行编译，以获得SIMD支持。如果你使用的是Cray，那么一种使用FFTW接口，  
经特殊修改（商业）版本的FFT，可以稍微快一些。

##### 使用 MKL

若目标为Intel CPU或GPU，可通过设置环境使用OneAPI MKL（>=2021\.3），例如通过source /  
opt/intel/oneapi/setvars\.sh或source /opt/intel/oneapi/mkl/latest/env/vars\.sh或手动设  
置环境变量sphinxupquoteMKLROOT=/full/path/to/mkl。然后设置\-DGMX\_FFT\_LIBRARY=mkl和/或  
\-DGMX\_GPU\_FFT\_LIBRARY=mkl后运行CMake。

##### 使用双批次 FFT 库

一般来说，MKL在Intel GPU上能提供更好的性能，但Intel提供的另一个开源库（https://github\.  
com/intel/double\-batched\-fft\-library）对于GROMACS中的超大FFT非常有用。

cmake\-DGMX\_GPU\_FFT\_LIBRARY=DBFFT\-DCMAKE\_PREFIX\_PATH=$PATH\_TO\_DBFFT\_INSTALL

##### 使用 ARM 性能库

ARM性能库为ARM架构提供了FFT变换的实现。通过提供与FFTW兼容的API，GROMACS为

ARMPL提供了初步支持。假定设置了ARM HPC工具链环境，其中包括ARMPL路径（例如可以通

过加载合适的模块，如module load Module\-Prefix/arm\-hpc\-compiler\-X\.Y/armpl/X\.Y），那么可以  
使用下面的cmake选项：

cmake \-DGMX\_FFT\_LIBRARY=fftw3 \*\*  
\-DFFTWF\_LIBRARY=" $\{ ARMPL\_DIR \} /lib/libarmpl\_lp64\.so" \*\*  
\-DFFTWF\_INCLUDE\_DIR= $\{ ARMPL\_DIR \} /include

使用 ____cuFFTMp____

在使用CUDA构建时, NVIDIA GPU支持将PME工作分解到多个GPU上。这需要使用NVIDIA  
HPC SDK中的NVIDIAcuFFTMp \(cuFFT Multi\-process\)库↪https://docs\.nvidia\.com/hpc\-sdk/cufftmp构建GRO\-  
MACS,它可以跨多个计算节点分布FFT。要启用cuFFTMp支持，请使用以下cmake选项：

cmake\-DGMX\_USE\_CUFFTMP=ON \*\*  
\-DcuFFTMp\_ROOT=<pathtoNVIDIAHPCSDKmath\_libsfolder>

在尝试使用GPU PME分解功能之前，请确保满足 cuFFTMp的硬件和软件要求↪https://docs\.nvidia\.  
com/hpc\-sdk/cufftmp/usage/requirements\.html。此外，由于cuFFTMp内部使用 NVSHMEM↪https://developer\.nvidia\.com/  
nvshmem，因此建议参考 NVSHMEM FAQ页面↪https://docs\.nvidia\.com/hpc\-sdk/nvshmem/api/faq\.html\#general\-faqs，以  
了解运行时遇到的任何问题。

- 对于NVHPC SDK 23\.3或更高版本，基于cuFFTMp的PME分解构建会出现问题。要解决这个  
构建问题，可以在已安装CUDA驱动程序的节点上进行编译，或使用以下额外选项：

\-DCMAKE\_CXX\_FLAGS="\-L <PATH\_TO\_CUDA\_TOOLKIT>/lib64/stubs \-lnvidia\-ml \-lcuda"

使用 ____heFFTe____

构建GROMACS时,若将其链接到 heFFTe库↪https://icl\.utk\.edu/fft/，则可以将PME卸载到任何供应商的  
GPU上,从而将PME工作分解到多个GPU上。HeFFTe使用GPU感知的MPI来提供分布式FFT，  
包括跨多个计算节点的FFT。对NVIDIA GPU，需要CUDA构建；对Intel或AMD GPU，则需要  
SYCL构建。要启用heFFTe支持，请使用以下cmake选项：

cmake\-DGMX\_USE\_HEFFTE=ON \*\*  
\-DHeffte\_ROOT=

你需要安装一个heFFTe，配置其所使用的GPU感知MPI库与GROMACS将使用的相同，并且支  
持与GROMACS的预期构建相匹配。最好也使用相同的C\+\+编译器和标准库。当使用Intel GPU  
时，添加\-DHeffte\_ENABLE\_ONEAPI=ON \-DHeffte\_ONEMKL\_ROOT=\. 当使用  
AMD GPU时，添加\-DHeffte\_ENABLE\_ROCM=ON \-DHeffte\_ROCM\_ROOT=。

使用 ____VkFFT____

VkFFT↪https://github\.com/DTolm/VkFFT是一个多后端GPU加速多维快速傅立叶变换库，旨在为供应商库提  
供一个开源的替代方案。

GROMACS支持VkFFT有两个目标：跨GPU平台的可移植性和性能改善。VkFFT可与OpenCL和  
SYCL后端一起使用：

- 对于SYCL的构建，VkFFT提供了一个可移植的后端，目前可通过hipSYCL在AMD和NVIDIA  
GPU上使用；它的性能通常优于rocFFT，因此在AMD上建议作为默认。注意，VkFFT不支持  
PME分解（需要HeFFTe），因为HeFFTe没有VkFFT后端。
- 对于OpenCL构建，VkFFT提供了ClFFT的替代方案。在macOS上和使用Visual Studio构  
建时,它是默认的。在其他平台上，VkFFT尚未经过广泛测试，但其性能可能优于ClFFT，可在  
cmake配置过程中启用。

要启用VkFFT支持,使用下面的CMake选项:

cmake\-DGMX\_GPU\_FFT\_LIBRARY=VKFFT

GROMACS将VkFFT与其源代码捆绑在一起，但也可以通过以下方式使用外部VkFFT（例如，从比  
捆绑版本更新的VkFFT发布中获益）：

cmake\-DGMX\_GPU\_FFT\_LIBRARY=VKFFT \*\*  
\-DGMX\_EXTERNAL\_VKFFT=ON\-DVKFFT\_INCLUDE\_DIR=

#### 2\.2\.6 其他可选的构建组件

- 链接hwloc可以提高硬件功能的运行时检测\.默认关闭此选项,因为可能不是所有地方都支持,但  
如果安装了hwloc,设置\-DGMX\_HWLOC=ON应该可以启用。
- 硬件优化的BLAS和LAPACK库对于一些侧重于简正模式和矩阵操作的GROMACS实用程序  
非常有用，但不会为正常模拟提供任何好处。相关配置将在线性代数库↪ 22 中进行讨论。
- 通过设置 \-DGMX\_EXTERNAL\_TNG=yes可以使用处理轨迹文件的外部TNG库，但GROMACS源  
码中已经自带了TNG 1\.7\.10。
- GROMACS使用lmfit库进行Levenberg\-Marquardt曲线拟合。只支持lmfit 7\.0。GROMACS发  
布中自带了该库的简化版，默认构建时会使用它。默认设置可以通过\-DGMX\_USE\_LMFIT=INTERNAL  
明确地启用。要使用外部lmfit库，请设置\-DGMX\_USE\_LMFIT=external，并根据需要调整CMAKE\_\-  
PREFIX\_PATH。可以使用\-DGMX\_USE\_LMFIT=none来禁用lmfit支持。
- TNG使用zlib来压缩某些类型的轨迹数据
- GROMACS 文 档 的 构 建 是 可 选 的， 构 建 时 需 要 其 他 软 件\. 请 参 考https://  
manual\.gromacs\.org/current/dev\-manual/documentation\-generation\.html 或源码中的 docs/  
dev\-manual/documentation\-generation\.rst文件。
- GROMACS实用程序输出数据文件时通常采用适合Grace绘图工具的格式，但将它们用于其他绘  
图程序也很简单。
- 在使用CMake配置GROMACS时，设置\-DGMX\_PYTHON\_PACKAGE=ON可从GROMACS的CMake  
主构建中为gmxapi Python包和sample\_restraint包启用额外的CMake目标。这会支持额外的  
测试和文档生成。

### 2\.3 构建 GROMACS

本节将介绍使用 CMake ↪ 10 构建GROMACS的一般过程，但不会详细讨论如何使用CMake。网上有许  
多资源，我们建议在遇到此处未涉及的问题时先搜索网络资源。下面的材料专门用于类Unix系统上的  
构建，包括Linux和Mac OS X。对于其他平台，请参阅下面的特殊说明。

#### 2\.3\.1 使用 CMake 进行配置

CMake会在系统上运行许多测试，并尽量解决如何构建GROMACS的问题。如果构建所用的机器与目  
标机器相同，那么可以确信默认值和检测结果非常好。但是，如果要控制构建的各个方面，或者要在集  
群的头节点上为具有不同架构的后端节点进行编译，则需要考虑指定的一些内容。

使用CMake配置GROMACS的最佳方法是，创建另一个运行CMake的目录，然后进行源外构建。这个  
目录可以在源代码目录之外，也可以是其子目录。这也意味着你永远不会在尝试构建源代码时破坏源代  
码\!因此，CMake命令行上唯一必需的参数是目录名称，其中包含用于要构建的代码的CMakeLists\.txt  
文件。例如，下载源代码压缩包，然后使用

tar xfz gromacs\-2019\.6\.tgz  
cd gromacs\-2019\.  
mkdir build\-gromacs  
cd build\-gromacs  
cmake \.\.

可以看到cmake报告了由GROMACS构建系统完成的一系列测试和检测结果。这些会写入cmake缓  
存，保存在 CMakeCache\.txt中。你可以手动编辑此文件，但不建议这样做，因为你可能会引入错误。  
你不应尝试移动或复制此文件来进行其他构建，因为其中的文件路径是固定的。如果弄错了，只需删除  
这个文件，然后用cmake重新开始。

如果在这个阶段检测到严重问题，你会看到致命错误以及关于如何解决它们的一些建议。如果你不  
确定如何处理，请先在网上搜索一下（大多数计算机问题都有已知的解决方案\!），然后查阅用户论  
坛↪https://gromacs\.bioexcel\.eu/c/gromacs\-user\-forum/5。输出中也有一些警告信息，你可能愿意接受或不接受它们。使  
用less或tee管道cmake的输出也很有用。

一旦cmake完成，你就可以看到所选的所有设置及其信息，方法是使用其他界面

ccmake \.\.

实际上，在第一步中你可以直接使用ccmake（大多数Unix平台上都可用），但这种情况下大多数状态  
消息只会显示在终端的下半部分，而不会写入标准输出。包括Linux，Windows和Mac OS X在内的  
大多数平台甚至都有cmake的原生图形用户界面，它可以为几乎任意的构建环境（包括Visual Studio  
或Xcode）创建项目文件。查看 CMake运行说明↪http://www\.cmake\.org/runningcmake/，了解相关界面以及如何  
导航和更改内容的一般建议。通常你可能想要更改的设置已经显示了。你可以进行更改，然后重新配置  
（使用c），这样它就可以根据你的更改进行改变并执行更多检查。可能需要进行多次配置才能得到所需  
的配置，特别是在需要解决错误的情况下。  
当你使用 ccmake得到所需的配置后，可以按下 g来生成构建系统。这要求先前的配置没有改变任何  
其他设置（如果有改变，则需要再次使用c进行配置）。使用cmake，每次没有产生错误的过程都会生  
成构建系统。  
首次运行cmake之后，无法再改变编译器。如果需要更改，可以清理并重新开始。

##### GROMACS 的安装位置

##### GROMACS安装在CMAKE\_INSTALL\_PREFIX指向的目录中。它可能不是源代码目录或构建目录。对此

##### 目录你需要具有写权限。因此，如果没有超级用户权限，CMAKE\_INSTALL\_PREFIX必须在你的家目录中。

##### 即使拥有超级用户权限，你也应该只在安装阶段使用，而不能将其用于配置，构建或运行GROMACS\!

使用 CMake 命令行选项

熟悉设置和更改选项后，你可能会提前知道如何配置GROMACS。如果这样，你可以通过调用cmake

并在命令行上一次传递各种选项来加快速度。这可以通过在调用cmake时使用 \-DOPTION=VALUE设置

缓存变量来完成。注意，也会考虑一些环境变量，特别是像CC和CXX这样的变量。

例如，以下命令行

cmake \.\. \-DGMX\_GPU=CUDA \-DGMX\_MPI=ON \-DCMAKE\_INSTALL\_PREFIX=/home/marydoe/programs

可用于使用CUDA GPU，MPI的构建并安装在自定义的位置。你甚至可以将其保存在shell脚本中，这

样下次使用时更容易。也可以使用ccmake 来进行，但你应该避免这种情况，因为在ccmake运行时无

法以交互方式更改用\-D设置的选项。

##### SIMD 支持

GROMACS对检测和使用许多现代HPC CPU架构的SIMD功能提供了广泛的支持。如果正在构建的

GROMACS会运行在相同的硬件上，那么你不需要阅读更多相关内容，除非你遇到了不明白的配置警

告。默认情况下，GROMACS构建系统会检测（配置所用的）CPU架构支持的SIMD指令集，从而选

择GROMACS支持的最佳的可用SIMD并行化。构建系统还会检查所用的编译器和链接器是否也支持

所选的SIMD指令集，如果不支持会导致致命错误。

下面列出了SIMD的有效值，通常你应该选择列表中编号最大的适用值。在大多数情况下，选择不合

适的较高数字会导致编译的二进制文件无法运行。但是，对许多处理器架构，如Intel Skylake\-X/SP和

AMD Zen\(第一代\)，选择最高的支持值会导致性能损失。

None仅用于缺少SIMD或GROMACS尚未移植的架构，以下选项均不适用。

SSE2这套SIMD指令集于 2001 年在Intel处理器中引入，并于 2003 年引入AMD处理器。基本  
上，现存的所有x86机器都支持此指令集，因此，如果你需要支持老旧的x86计算机，它可能是  
一个不错的选择。

SSE4\.1自 2007 年以来所有Intel核心处理器都支持，但值得注意的是，AMD Magny\-Cours不支  
持。尽管如此，几乎所有新近的处理器都支持它，因此如果你不介意模拟速度，并且更关心在相当  
现代的处理器之间的可移植性，那么这个设置也可以作为一个很好的选择基准。

AVX\_128\_FMAAMD Bulldozer，Piledriver（以及后来的Family 15h）处理器都支持,但自Zen1开  
始的任何AMD处理器都 不 再支持。

AVX\_256自Sandy Bridge（ 2011 ）以来的Intel处理器。虽然这一选项也适用于AMD Bulldozer  
和Piledriver处理器，但它的效率显著低于上面的AVX\_128\_FMA选项\-在这种情况下，不要盲目  
地假定 256 优于 128 。

AVX2\_128AMD Zen/Zen2以及Hygon Dhyana微架构处理器;它将使AVX2具有 3 路融合乘加  
指令。虽然这些微架构确实支持 256 位AVX2指令，因此也支持 AVX2\_256。但 128 位通常会  
更快，特别是当非键任务在CPU上运行时\-因此默认为 AVX2\_128。然而，使用GPU卸载时，  
AVX2\_256在Zen处理器上可以更快。

AVX2\_256Intel Haswell（及更高版本）处理器（ 2013 ）以及AMD Zen3及其后续\(2020\)支持\.它  
还会启用Intel 3路融合乘加指令。

AVX\_512Skylake\-X台式机和Skylake\-SP Xeon处理器（ 2017 年）以及AMD Zen4\(2022\);在Intel  
上,通常在具有两个 512 位融合乘加单元的高端桌面和服务器处理器上最快（例如，Core i9和  
Xeon Gold）。但是，某些桌面和服务器型号（例如Xeon Bronze和Silver）只配备了一个AVX  
FMA单元，因此在这些处理器上AVX2\_256更快（编译和运行时检查会尝试告知这些情况）。在  
AMD上,自Zen4开始使用是有益的\.此外，使用GPU加速运行AVX2\_256在启用了两个 512 位  
FMA单元的高端Skylake CPU上也可以更快。

IBM\_VSXPower7，Power8，Power9及更高版本支持。

ARM\_NEON\_ASIMD 64 位ARMv8及更高版本。

ARM\_SVE使用可扩展向量扩展（SVE）的 64 位ARMv8及更高版本。SVE向量长度是在CMake  
配置时固定的。会自动检测默认向量长度，但可通过CMake变量GMX\_SIMD\_ARM\_SVE\_LENGTH更  
改。所需的最低编译器版本为GNU >= 10）、LLVM >= 13或ARM >= 21\.1。为获得最高性能，  
我们强烈建议使用最新的gcc编译器，或至少使用LLVM 14或ARM 22\.0。以及观察到LLVM 13  
和ARM编译器21\.1的性能较低。

CMake配置系统会检查你选择的编译器是否可以用于所选的架构。mdrun在运行时会进一步检查，因  
此如果有疑问，请选择你认为可能有效的最低数字，然后查看mdrun给出的说明。配置系统还可以解决  
许多常见HPC编译器版本中的许多已知问题。

还有一个 GMX\_SIMD=Reference选项，这是一个特殊的类似SIMD的实现，用简单的C编写，开发  
人员为新的SIMD架构开发GROMACS支持时可以使用它。它并不是为成品模拟而设计的，但如果  
你所用的架构支持SIMD而GROMACS尚未移植到其上，你可能希望试试此选项而不是使用默认的  
GMX\_SIMD=None，因为当编译器中的自动向量化做得很好时，这样做性能通常会更好。成功后请发布到  
GROMACS 用户论坛↪https://gromacs\.bioexcel\.eu/c/gromacs\-user\-forum/5，这样GROMACS可能会在几天内移植到  
新的SIMD架构上。

CMake 高级选项

在ccmake 默认视图中显示的选项是我们认为大多数用户可能会考虑更改的选项。还有更多可用的选

项，你可以使用t切换到 ccmake的高级模式进行查看。即便如此，你可能想要更改的大多数变量都

有CMAKE\_或GMX\_前缀。还有一些选项会根据其先决条件是否满足而显示或不显示。

帮助 CMake 找到正确的库，头文件或程序

如果库没有安装在默认位置，则可以使用以下变量指定其位置：

CMAKE\_INCLUDE\_PATH用于头文件

CMAKE\_LIBRARY\_PATH用于库

CMAKE\_PREFIX\_PATH用于头文件，库和二进制文件（例如 /usr/local）。  
相应的include，lib或bin 会附加到路径中。这些变量中的每一个都可以指定一个路径列表（在  
Unix上，用: 分隔）。可以将这些变量设置为环境变量，如下所示：

CMAKE\_PREFIX\_PATH=/opt/fftw:/opt/cuda cmake \.\.

（假定shell为bash）。或者，这些变量也是cmake选项，因此可以将它们设置为\-DCMAKE\_PREFIX\_\-  
PATH=/opt/fftw:/opt/cuda。  
CC和CXX环境变量也很有用，它们用以指示cmake要使用的编译器。类似地，CFLAGS/CXXFLAGS可  
用于传递编译器选项，但请注意，这些选项会附加到GROMACS为你的构建平台和构建类型而设置的  
选项中。你可以使用CMake高级选项，如CMAKE\_C\_FLAGS及其相关选项来自定义其中的一些选项。  
另请参阅 CMake环境变量↪http://cmake\.org/Wiki/CMake\_Useful\_Variables\#Environment\_Variables 页面。

##### CUDA GPU 加速

如果安装了 CUDA↪http://www\.nvidia\.com/object/cuda\_home\_new\.html 工具包，可以这样使用cmake:

cmake \.\. \-DGMX\_GPU=CUDA \-DCUDA\_TOOLKIT\_ROOT\_DIR=/usr/local/cuda

（或安装的任何路径）。在某些情况下，你可能需要手动指定应该使用哪一个C\+\+编译器，例如，使用  
高级选项CUDA\_HOST\_COMPILER。  
默认情况下，将会为最常见的CUDA架构生成代码。但是，为了减少构建时间和二进制大小，我们不  
会为每个可能的架构生成代码，在极少数情况下（例如，Tegra系统）可能导致默认构建无法使用某些  
GPU。如果发生这种情况，或者如果要删除某些架构以减少二进制文件大小和构建时间，你可以更改目  
标CUDA的架构。这可以使用GMX\_CUDA\_TARGET\_SM或GMX\_CUDA\_TARGET\_COMPUTECMake变量来完  
成，它使用由分号分隔的字符串，含有CUDA（虚拟）架构名称的两位数字后缀，例如360;75;86。详  
细信息，请参阅nvcc文档/帮助页的“Options for steering GPU code generation”部分，或nvcc手册  
的第 6 章。  
GPU加速已经在使用Linux，Mac OS X和Windows操作系统的AMD64/x86\-64平台上进行了测试，  
但Linux是其中测试和支持最好的。在POWER 8/9，ARM V8 CPU上运行的Linux也工作得很好。  
可以使用CLANG（6\.0或更高版本）为主机和设备编译CUDA代码提供实验支持。这种情况下仍然需  
要CUDA工具包，但它仅用于生成GPU设备代码并链接到CUDA运行时库。clang CUDA支持简化  
了编译并为开发提供了便利（例如允许在CUDA主机代码中使用代码清理程序）。此外，使用clang进

行CPU和GPU编译有助于避免GNU工具链和CUDA工具包之间的兼容性问题。可以使用CMake

选项GMX\_CLANG\_CUDA=ON来启用CUDA的clang。可以使用 GMX\_CUDA\_TARGET\_SM来选择目标架构，

虚拟架构代码始终会嵌入所有请求的架构（因此会忽略GMX\_CUDA\_TARGET\_COMPUTE）。请注意，这主要

是一个面向开发人员的特性，但其性能通常接近使用nvcc编译的代码\.

OpenCL GPU 加速

GROMACS支持OpenCL的主要目的在于加速AMD和Intel硬件的模拟。对于AMD，我们的目标  
是分开的GPU和APU（集成CPU\+GPU芯片），而对于Intel，我们的目标是现代工作站和移动硬件  
上的集成GPU。NVIDIA GPU上的GROMACS OpenCL工作正常，但性能和其他限制使其不太实用  
（详细信息请参见用户指南）。

要在启用 OpenCL↪https://www\.khronos\.org/opencl/ 支持的情况下构建 GROMACS，需要两个组件：

OpenCL↪https://www\.khronos\.org/opencl/ 头文件和作为客户端驱动程序加载器的封装库（所谓的ICD

加载器）。此外，针对设备的特定于供应商的GPU驱动程序只有在运行时才需要。这也包含

OpenCL↪https://www\.khronos\.org/opencl/ 编译器。由于GPU计算内核是在运行时根据需要编译的，因

此构建GROMACS时不需要特定于供应商的编译器和驱动程序。前者的编译时依赖项是标准组

件，因此可以从大多数Linux发行库获取库存版本（例如Debian/Ubuntu上的 opencl\-headers和

ocl\-icd\-libopencl1）。只需确保与所需 OpenCL↪https://www\.khronos\.org/opencl/ 版本1\.2兼容。或者，也可

以从供应商SDK获得头文件和库，但必须将其安装在 CMAKE\_PREFIX\_PATH中的路径中。

要启用 OpenCL↪https://www\.khronos\.org/opencl/ 构建，必须设置以下CMake选项

cmake \.\. \-DGMX\_GPU=OpenCL

要进行支持Intel集成GPU的构建，需要在cmake命令行中添加\-DGMX\_GPU\_NB\_CLUSTER\_Size=4，这

样GPU内核与硬件的特性才能匹配。推荐使用 Neo驱动程序↪https://github\.com/intel/compute\-runtime/releases。

在Mac OS上，AMD GPU只能用于OS 10\.10\.4及更高版本；已经知道早期的OS版本运行不正确。

默认情况下，Linux系统上的任何clFFT库都会与GROMACS一起使用，但如果找不到任何clfft库，

则代码将回退到GROMACS自带的版本。如果需要将GROMACS与外部库链接，请使用

cmake\.\.\-DGMX\_GPU=OpenCL\-DclFFT\_ROOT\_DIR=/path/to/your/clFFT \-DGMX\_EXTERNAL\_CLFFT=TRUE

On Windows with MSVC and on macOS, VkFFT↪https://github\.com/DTolm/VkFFT is used instead of clFFT,

but this can provide performance benefits on other platforms as well\.

在Windows上使用MSVC时,以及在macOS上，使用 VkFFT↪https://github\.com/DTolm/VkFFT 而不是

clFFT，但这也能为其他平台带来性能优势。

##### SYCL GPU 加速

SYCL↪https://www\.khronos\.org/sycl/是一种现代的可移植异构加速API，针对不同的硬件平台有多种实现（类

似于 OpenCL↪https://www\.khronos\.org/opencl/）。

GROMACS可与不同的SYCL编译器/运行时配合使用，并以下列硬件为目标：

- 使用 Intel oneAPI DPC\+\+↪https://www\.intel\.com/content/www/us/en/developer/tools/oneapi/dpc\-compiler\.html的Intel  
GPU（OpenCL和LevelZero后端）
- 使用 hipSYCL↪https://github\.com/illuhad/hipSYCL 的AMD GPU（仅独立GPU）

##### 此外，还试验性地支持

- 使用Codeplay oneAPI for AMD GPUs↪https://developer\.codeplay\.com/products/oneapi/amd/home/的AMD GPU
- 使用 hipSYCL↪https://github\.com/illuhad/hipSYCL或 Codeplay oneAPI for NVIDIA GPUs↪https://developer\.  
codeplay\.com/products/oneapi/nvidia/home/ 的NVIDIA GPU

以表格形式汇总如下:

##### GPU

##### 供应商

hipSYCL↪https:

//github\.com/illuhad/hipSYCL

Intel oneAPI DPC\+\+↪https://www\.intel\.com/content/

www/us/en/developer/tools/oneapi/dpc\-compiler\.html

Codeplay oneAPI↪https://developer\.

codeplay\.com/products/oneapi/nvidia/home/

Intel 不支持 支持 试验性\(需要安装MKL\)

AMD 支持 不支持 试验性\(无GPU FFT\)

NVIDIA试验性 不支持 试验性\(无GPU FFT\)

这里的”试验性支持”意味着指该组合已经过有限测试，预计可以正常工作（可能有局限性），但不建议

用于实际生产。

GROMACS中的SYCL↪https://www\.khronos\.org/sycl/支持旨在最终取代OpenCL↪https://www\.khronos\.org/opencl/作  
为AMD和Intel硬件的加速机制。

对于NVIDIA GPU，我们强烈建议使用 CUDA。SYCL 不支持苹果M1/M2 GPU，但可以使用  
OpenCL↪https://www\.khronos\.org/opencl/。

Codeplay ComputeCpp is not supported\. Open\-source Intel LLVM↪https://github\.com/intel/llvm can be used  
in the same way as Codeplay oneAPI for targeting AMD/NVIDIA devices\.

不支持Codeplay ComputeCpp。开源的Intel LLVM↪https://github\.com/intel/llvm可用于AMD/NVIDIA设备,  
使用方式与Codeplay oneAPI相同。

注意：GROMACS中的SYCL↪https://www\.khronos\.org/sycl/支持以及底层编译器和运行时都不如OpenCL或  
CUDA成熟。恳请,使用时要格外注意模拟的正确性。

____Intel GPU____ 的 ____SYCL GPU____ 加速

你应安装最新的Intel oneAPI DPC\+\+↪https://www\.intel\.com/content/www/us/en/developer/tools/oneapi/dpc\-compiler\.html编  
译器工具包。对于GROMACS 2023，推荐使用2022\.3版。使用开源的Intel LLVM↪https://github\.com/intel/  
llvm也是可行的，但尚未经过广泛测试。我们还建议安装最新的 Neo驱动程序↪https://github\.com/intel/  
compute\-runtime/releases。

安装工具包将其添加到环境后（通常通过运行source /opt/intel/oneapi/setvars\.sh,或在HPC系  
统上使用适当的 ____module load____ ），必须设置以下CMake标记：

cmake\.\.\-DCMAKE\_C\_COMPILER=icx\-DCMAKE\_CXX\_COMPILER=icpx\-DGMX\_GPU=SYCL

在为Intel Data Center GPU Max（也称为Ponte Vecchio / PVC）编译时，我们建议传递额外的标记以  
提高兼容性和性能：

cmake\.\.\-DCMAKE\_C\_COMPILER=icx\-DCMAKE\_CXX\_COMPILER=icpx\-DGMX\_GPU=SYCL \*\*  
\-DGMX\_GPU\_NB\_NUM\_CLUSTER\_PER\_CELL\_X= 1 \-DGMX\_GPU\_NB\_CLUSTER\_SIZE= 8

你也可以考虑使用双批次 FFT 库。

##### AMD GPU 的 SYCL GPU 加速

建议使用 hipSYCL 0\.9\.4↪https://github\.com/illuhad/hipSYCL/releases/tag/v0\.9\.4 和ROCm 5\.3\-5\.4。我们强烈建议使  
用ROCm捆绑的clang编译器来构建hipSYCL和GROMACS。主线Clang版本也可以使用。

配置 ____hipSYCL____ 时，可以使用以下CMake命令以确保使用正确的Clang（假定ROCM\_PATH设置正确，  
例如在默认安装的情况下设置为/opt/rocm ）：

cmake\.\.\-DCMAKE\_C\_COMPILER= $\{ ROCM\_PATH \} /llvm/bin/clang \*\*  
\-DCMAKE\_CXX\_COMPILER= $\{ ROCM\_PATH \} /llvm/bin/clang\+\+ \*\*  
\-DLLVM\_DIR= $\{ ROCM\_PATH \} /llvm/lib/cmake/llvm/

如果使用的是ROCm 5\.0或更早版本，hipSYCL可能需要 额外的构建标记↪https://github\.com/illuhad/hipSYCL/  
blob/v0\.9\.4/doc/install\-rocm\.md。

编译并安装hipSYCL后，以下设置可用于构建GROMACS本身（将 HIPSYCL\_TARGETS 设为目标硬  
件）：

cmake\.\.\-DCMAKE\_C\_COMPILER= $\{ ROCM\_PATH \} /llvm/bin/clang \*\*  
\-DCMAKE\_CXX\_COMPILER= $\{ ROCM\_PATH \} /llvm/bin/clang\+\+ \*\*  
\-DGMX\_GPU=SYCL\-DGMX\_SYCL\_HIPSYCL=ON \-DHIPSYCL\_TARGETS='hip:gfxXYZ'

可以指定多个目标架构，例如：\-DHIPSYCL\_TARGETS='hip:gfx908,gfx90a'。在同一构建中同时具有  
RDNA（gfx1xyz）和GCN/CDNA（gfx9xx）设备也是可能的，但与只为GCN/CDNA设备进行的  
构建相比，性能会略有下降。如果同一系统中有多个不同世代的AMD GPU（例如，集成APU和独立  
GPU），ROCm运行时需要在运行时能为每个设备提供代码，因此编译时需要在 HIPSYCL\_TARGETS中  
指定每个设备，以避免ROCm在初始化时崩溃。

默认情况下，VkFFT↪https://github\.com/DTolm/VkFFT用于在GPU上执行FFT。你可以通过传递CMake标  
记\-DGMX\_GPU\_FFT\_LIBRARY=rocFFT 以切换到rocFFT。请注意，rocFFT并未获得官方支持，而且往  
往无法在大多数消费级GPU上运行。

AMD GPU也可以使用 Codeplay oneAPI for AMD GPU↪https://developer\.codeplay\.com/products/oneapi/amd/home/，  
但这是试验性的，不支持将FFT卸载到GPU。安装Intel oneAPI工具包2023\.0或更新版本、兼容  
的ROCm版本和Codeplay插件后，运行sphinxcodesource /opt/intel/oneapi/setvars\.sh \-\-include\-intel\-  
llvm或在HPC系统上加载适当的 ____module load____ 。然后，使用以下命令配置GROMACS（将gfxXYZ  
替换为目标架构）：

cmake\.\.\-DCMAKE\_C\_COMPILER=clang\-DCMAKE\_CXX\_COMPILER=clang\+\+ \*\*  
\-DGMX\_GPU=SYCL\-DGMX\_GPU\_NB\_CLUSTER\_SIZE= 8 \-DGMX\_GPU\_FFT\_LIBRARY=none \*\*  
\-DSYCL\_CXX\_FLAGS\_EXTRA='\-fsycl\-targets=amdgcn\-amd\-amdhsa;\-Xsycl\-target\-backend;\-\-  
↪offload\-arch=gfxXYZ'

##### NVIDIA GPU 的 SYCL GPU 加速

对NVIDIA GPU的SYCL支持是高度试验性的。对于生产，请使用 CUDA↪https://developer\.nvidia\.com/

cuda\-zone \( CUDA GPU 加速\)。

NVIDIA GPU 可以与 hipSYCL↪https://github\.com/illuhad/hipSYCL or Codeplay oneAPI for NVIDIA

GPUs↪https://developer\.codeplay\.com/products/oneapi/nvidia/home/ 一起使用。

对于hipSYCL，请确保hipSYCL自身在编译时支持CUDA，并通过 HIPSYCL\_TARGETS提供适当的设

备\(例如, \-DHIPSYCL\_TARGETS=cuda:sm\_75\)。在编译CUDA时，我们建议使用主线Clang，而不是

ROCm捆绑的Clang。

对于 Codeplay oneAPI for NVIDIA GPUs↪https://developer\.codeplay\.com/products/oneapi/nvidia/home/，安装In\-

tel oneAPI toolkit 2023\.0或更新版本以及Codeplay插件，通过运行 source /opt/intel/oneapi/

setvars\.sh \-\-include\-intel\-llvm 或在HPC系统上加载适当的 module load 设置环境。然后，使

用以下命令配置GROMACS：

cmake\.\.\-DCMAKE\_C\_COMPILER=clang\-DCMAKE\_CXX\_COMPILER=clang\+\+ \\

\-DGMX\_GPU=SYCL\-DGMX\_GPU\_NB\_CLUSTER\_SIZE= 8 \-DGMX\_GPU\_FFT\_LIBRARY=none \\

\-DSYCL\_CXX\_FLAGS\_EXTRA=\-fsycl\-targets=nvptx64\-nvidia\-cuda

##### SYCL GPU 编译选项

为了微调GROMACS，可以向CMake传递以下标记：  
\-DGMX\_GPU\_NB\_CLUSTER\_SIZE  
改变非键内核的数据布局。使用Intel oneAPI DPC\+\+↪https://www\.intel\.com/content/www/us/en/developer/tools/  
oneapi/dpc\-compiler\.html进行编译时，默认值为 4 ，这对于大多数Intel GPU来说都是最佳值,但对于  
Intel Data Center MAX \(Ponte Vecchio\) 8会更好。使用 hipSYCL↪https://github\.com/illuhad/hipSYCL编  
译时，默认值为 8 ，AMD和NVIDIA设备只支持此值。  
\-DGMX\_GPU\_NB\_NUM\_CLUSTER\_PER\_CELL\_X, \-DGMX\_GPU\_NB\_NUM\_CLUSTER\_PER\_CELL\_Y,  
\-DGMX\_GPU\_NB\_NUM\_CLUSTER\_PER\_CELL\_Z

设置成对搜索网格单元中沿X、Y或Z方向的簇数，默认为 2 。当针对Intel Ponte Vecchio GPU

时，设置\-DGMX\_GPU\_NB\_NUM\_CLUSTER\_PER\_CELL\_X=1并将其他值保留为默认值。

\-DGMX\_GPU\_NB\_DISABLE\_CLUSTER\_PAIR\_SPLIT

在GPU非键内核中禁用簇成对拆分。只有SYCL支持该选项,对于64\-wide execution的GPU,

如AMD GCN和CDNA系列,兼容并能提高其GPU性能。在所有以GCN或CDNA GPU（但

不包括RDNA）为目标的构建中，该选项都会自动启用。

##### 静态链接

##### 安装后，动态链接的GROMACS可执行文件占用的磁盘空间更少，因此对我们认为已进行过重复测试

并工作正常的平台，动态链接是默认设置。一般来说，这包括Linux，Windows，MacOSX和BSD系

统。静态二进制文件占用更多空间，但在某些硬件和/或某些条件下推荐使用,或有必要使用，最常见的

情况是使用MPI库运行并行模拟时（例如Cray）。

- 要将GROMACS二进制文件静态链接到内部GROMACS库，请设置\-DBUILD\_SHARED\_LIBS=OFF。
- 如果也要对外部（非系统）库进行静态链接，请设置\-DGMX\_PREER\_STATIC\_LIBS=ON。注意，通  
常cmake会任意选择一种可行的方式，所以此选项只是指示 cmake在静态和共享都可用时偏向  
静态库。如果一个外部库没有可用的静态版本，即使上述选项为ON，也会使用共享库。另请注意，  
生成的二进制文件仍将动态链接到平台上的系统库，这是默认情况。要使用静态系统库，需要额外  
的编译器/链接器选项，例如，\-static\-libgcc \-static\-libstdc\+\+。
- 如果要试着链接一个完全静态的二进制文件，请设置\-DGMX\_BUILD\_SHARED\_EXE=OFF。这会防止  
CMake明确地设置任何动态链接选项。默认情况下，此选项还会设置\-DBUILD\_SHARED\_LIBS=OFF  
和\-DGMX\_PREER\_STATIC\_LIBS=ON，但上述注意事项仍适用。对于默认不是静态链接的编译器，必  
须指定所需的选项。在Linux上，通常是CFLAGS=\-static CXXFLAGS=\-static。

gmxapi C\+\+ API

对于动态链接构建，以及非Windows平台，可以通过设置 \-DGMXAPI=ON 安装额外的库和头文件  
（默认）。构建目标 gmxapi\-cppdocs 和gmxapi\-cppdocs\-dev 会分别在 docs/api\-user 和 docs/  
api\-dev中生成文档。更多项目信息和用例，请参阅问题跟踪 Issue 2585↪https://redmine\.gromacs\.org/issues/2585，  
关联GitHub gmxapi↪https://github\.com/kassonlab/gmxapi 项目，或DOI 10\.1093/bioinformatics/bty484↪https:  
//doi\.org/10\.1093/bioinformatics/bty484。  
gmxapi尚未对Windows或静态链接进行测试，但这些用例是针对未来版本的。

##### GROMACS 构建的可移植性

一个GROMACS构建通常无法移植，甚至不能在具有相同基本指令集的硬件上进行移植（如x86）。在

配置时选择不可移植的特定于硬件的优化，例如计算内核中使用的SIMD指令集，这会由构建系统根据

构建主机的功能完成，或者在配置过程中指定到cmake。

通常，可以通过选择SIMD支持的最小公共部分来确保可移植性，例如：x86使用SSE2\. 在非常

旧的x86机器的极少数情况下,如果任何目标CPU架构不支持RDTSCP 指令，请确保使用 cmake

\-DGMX\_USE\_RDTSCP=off。但是，在执行环境异构的情况下，如AVX和早期硬件混合使用，我们不鼓励

尝试使用单一的GROMACS安装版本，因为这会导致程序在新硬件上运行缓慢（尤其是mdrun）。构建

两个完整的安装版本，并在本机上管理如何调用正确的安装（例如使用module系统）是推荐的方法。或

者，也可以使用不同的后缀在同一位置安装几个GROMACS版本。为此，可以首先使用最小公共SIMD

指令集构建一个完整安装，例如，\-DGMX\_SIMD=SSE2，然后为异构环境中的每个架构构建特定的gmx二

进制文件。通过使用自定义的二进制文件和库后缀\(通过CMake变量 \-DGMX\_BINARY\_SUFFIX=xxx和

\-DGMX\_LIBS\_SUFFIX=xxx设定\),可以将它们安装到同一位置。

二进制文件在不同GPU之间的可移植性通常会更好，大多数情况下，只需一次GROMACS构建，就

能在同一供应商的多代GPU上运行。默认情况下，CUDA↪https://developer\.nvidia\.com/cuda\-zone 构建可在任

何NVIDIA GPU上运行,只要CUDA工具包支持即可,因为GROMACS构建系统会在构建时为这

些NVIDIA GPU生成代码。使用SYCL↪https://www\.khronos\.org/sycl/时，可以选择同一GPU供应商的多

个目标架构,若使用hipSYCL↪https://github\.com/illuhad/hipSYCL的话（即仅AMD或仅NVIDIA）。而使用  
OpenCL↪https://www\.khronos\.org/opencl/时，由于针对正使用设备的GPU代码的just\-in\-time编译，无需担心  
这一问题。

##### 线性代数库

如上所述，在执行简正模式分析或协方差分析时，有时供应商提供的BLAS和LAPACK库可以提

高GROMACS的性能。为简单起见，下面的文本仅提及BLAS，但LAPACK也提供了相同的选

项。默认情况下，CMake会搜索BLAS，如果找到就会使用它，否则使用GROMACS内部的BLAS  
版本。并相应地设置 cmake 选项 \-DGMX\_EXTERNAL\_BLAS=on。对于常规应用，内部版本完全可以胜  
任。如果需要指定搜索时的非标准路径，可以使用 \-DCMAKE\_PREFIX\_PATH=/path/to/search。如果  
需要指定的库具有非标准名称（例如Power机器上的ESSL或ARM机器上的ARMPL），可以设置  
\-DGMX\_BLAS\_USER=/path/to/reach/lib/libwhatever\.a。

如果你使用Intel MKL↪https://software\.intel\.com/en\-us/intel\-mkl 的FFT，则会自动使用它提供的BLAS和  
LAPACK。这可以使用GMX\_BLAS\_USER等选项覆盖。

在Apple平台上，如果可以使用Accelerate Framework，BLAS和LAPACK会自动使用它。这可以使  
用GMX\_BLAS\_USER等选项覆盖。

进行支持 MiMiC QM/MM 的构建

MiMiC QM/MM接口集成需要链接到MiMiC通信库，它可以建立GROMACS和CPMD之间的通信  
通道。MiMiC通信库可以在 这里↪https://gitlab\.com/MiMiC\-projects/CommLib 下载。编译并安装。如果安装在了  
非标准位置，请检查MiMiC库的安装目录是否添加到了 CMAKE\_PREFIX\_PATH。构建支持QM/MM的  
版本需要双精度版本的GROMACS并支持MPI:

\-DGMX\_DOUBLE=ON \-DGMX\_MPI \-DGMX\_MIMIC=ON

支持 CP2K QM/MM 的构建

CP2K QM/MM接口集成需要链接libcp2k库，该库可以将CP2K功能纳入GROMACS。

1\.下载、编译并安装CP2K（需要8\.1或更高版本）。

CP2K最新发行可在 此处↪https://github\.com/cp2k/cp2k/releases/下载。有关CP2K的具体安装说明，参见这  
里↪https://github\.com/cp2k/cp2k/blob/master/INSTALL\.md。也可以查看 CP2K官方页面↪https://www\.cp2k\.org/howto上的说  
明。

2\.执行下面的命令生成库文件 libcp2k\.a:

make ARCH=<your arch file> VERSION=<your version like psmp> libcp2k

库存档\(如libcp2k\.a\)应位于 /lib/ / /目录下\.

3\.使用 cmake 构建GROMACS,添加下面的标识

应进行静态构建: \-DBUILD\_SHARED\_LIBS=OFF \-DGMXAPI=OFF \-DGMX\_INSTALL\_NBLIB\_API=OFF

对QM/MM,双精度通常好于单精度\(但两种选项都是可行的\): \-DGMX\_DOUBLE=ON

CP2K和GROMACS之间的FFT, BLAS和LAPACK库应当相同,为此要使用以下标识:

\-DGMX\_FFT\_LIBRARY= \-DFFTWF\_LIBRARY=

\-DFFTWF\_INCLUDE\_DIR=<path to directory with headers>

\-DGMX\_BLAS\_USER=

\-DGMX\_LAPACK\_USER=  
4\.QM/MM接口的编译可以通过以下标识控制:

\-DGMX\_CP2K=ON

启用QM/MM接口编译

\-DCP2K\_DIR="/lib/local/psmp

libcp2k\.a库所在的目录

\-DCP2K\_LINKER\_FLAGS=""\( 对 CP2K 9\.1 或更新为可选项 \)

CP2K使用的其他库。通常情况下，这应该是编译CP2K所用ARCH文件中的LDFLAGS和

LIBS的组合。有时，ARCH文件中定义LDFLAGS和LIBS的内容可能有多行，甚至还使用\\将

一行分割为多行。在这种情况下，应将所有这些字符串连接成一个长字符串，并去除其中所有额外

的斜线或引号。对于9\.1或更新版本的CP2K，CP2K\_LINKER\_FLAGS并不是必需的，但在非常特

殊的情况下仍有可能会用到。

##### 更改 GROMACS 二进制文件和库的名称

##### 有时安装同一GROMACS程序的不同版本很方便。最常见的情况是单精度和双精度版本，以及使用和

不使用MPI的版本。正如前面提到的，这种机制还可以用于安装针对不同CPU架构优化的多个mdrun

版本。

默认情况下，GROMACS会为构建的此类程序和库添加后缀\_d 表示双精度和/或\_mpi表示MPI（除

此之外不会添加其他内容）。可以使用 GMX\_DEFAULT\_SUFFIX \(ON/OFF\)，GMX\_BINARY\_SUFFIX（接受

字符串）和GMX\_LIBS\_SUFFIX（也接受字符串）手动控制这一点。例如，要为程序和库设置自定义后

缀，可以指定：

cmake \.\. \-DGMX\_DEFAULT\_SUFFIX=OFF \-DGMX\_BINARY\_SUFFIX=\_mod \-DGMX\_LIBS\_SUFFIX=\_mod

这样，所有程序和库的名称都会附加\_mod。

##### 更改安装树结构

默认情况下，安装GROMACS时，会使用CMAKE\_INSTALL\_PREFIX下的几个不同目录。其中的一些可

以更改，这主要用来打包GROMACS用于各种发行版。下面列出了这些目录，并对其中一些做了附加

说明。除非另有说明，否则可以通过编辑主CMakeLists\.txt中的安装路径来重命名目录。

bin/ 可执行文件和一些脚本的标准位置。某些脚本的绝对安装前缀使用了硬编码，如果脚本的位置发

生了变化，需要更改前缀。可以使用CMake变量CMAKE\_INSTALL\_BINDIR来更改目录的名称。

include/gromacs/ 头文件的标准安装位置。

lib/ 库的标准位置。默认值取决于系统，由CMake确定。可以使用CMake变量 CMAKE\_INSTALL\_\-

LIBDIR更改目录的名称。

lib/pkgconfig/ 此处安装了为pkg\-config安装的libgromacs库的信息。lib/部分地适应库的安

装位置。已安装的文件包含安装前缀作为绝对路径。

share/cmake/ CMake软件包配置文件安装在此处。

share/gromacs/ 这里存放各种数据文件和一些文档。第一部分可以使用CMAKE\_INSTALL\_DATADIR进

行更改，第二部分可以使用 GMX\_INSTALL\_DATASUBDIR进行更改。使用这些CMake变量是更改

share/gromacs/top/安装路径的首选方法，因为这个目录的路径内置于libgromacs 以及一些

脚本中，既可以作为相对路径，也可以作为绝对路径（如果其他的失败，绝对路径可以作为备用路

径）。

share/man/ 安装的手册页放在这里。

#### 2\.3\.2 编译和链接

一旦使用cmake 完成了配置，就可以使用 make构建GROMACS。预计这一操作总会成功完成，并  
且很少或没有警告。GROMACS对你所选的设置进行了非常广泛的CMake测试，但可能仍然会有  
一些我们没有考虑到的情况。首先搜索网络寻找问题的解决方案，但如果你需要帮助，请到用户论  
坛↪https://gromacs\.bioexcel\.eu/c/gromacs\-user\-forum/5提问，并提供尽可能多的信息，如你做了什么，正在构建的系统  
是什么，以及出错的信息。这可能意味着在make的输出中向后滚动很长一段才能找到第一条错误消息\!

如果你有一台有N个处理器的多核或多CPU机器，那么使用

make \-j N

通常会快很多。cmake 支持的其他构建生成器系统（例如ninja）也可以正常使用。

#### 2\.3\.3 安装 GROMACS

最后，make install会将GROMACS安装到CMAKE\_INSTALL\_PREFIX指定的目录中。如果这是一个  
系统目录，那么你需要具有写权限，并且你应该只在make install过程中使用超级用户权限，而不要  
在整个过程中都使用。

#### 2\.3\.4 安装后使用 GROMACS

GROMACS会在安装目录的bin子目录（例如/usr/local/gromacs/bin/GMXRC）中安装脚本GMXRC，  
你可以在shell中使用source执行它：

source/your/installation/prefix/here/bin/GMXRC

它会检测正在运行的shell类型，并设置好使用GROMACS的环境。你可能希望将此操作放入登录脚本  
中以便自动执行；请到网上搜索不同shell的操作说明。

许多GROMACS程序运行时需要读取安装目录的share/gromacs子目录中的数据。默认情况下，程  
序会使用 GMXRC脚本中设置的环境变量来确定这个目录的位置，如果没有设置环境变量，程序会试着  
根据自己的路径来猜测目录的位置。这种做法通常很有效，除非你更改了安装树中的目录名称。如果你  
仍然需要更改目录名称，你可能需要设置好正确的新安装位置并重新编译或编辑GMXRC脚本。

GROMACS还会安装CMake缓存文件，以帮助构建客户端软件（使用CMake配置客户端软件时，请  
使用\-C选项↪https://cmake\.org/cmake/help/latest/manual/cmake\.1\.html\#options）。如果安装在 /your/installation/  
prefix/here，提示文件将安装在/your/installation/prefix/share/cmake/gromacs$\{GMX\_LIBS\_\-  
SUFFIX\}/gromacs\-hints$\{GMX\_LIBS\_SUFFIX\}\.cmake其中$\{GMX\_LIBS\_SUFFIX\}为如上文所述\.

#### 2\.3\.5 测试 GROMACS 的正确性

自 2011 年以来，GROMACS开发使用了一个自动化系统，在这个系统中，每次新的代码更改都需要针

对许多平台和软件组合进行回归测试。虽然这大大提高了可靠性，但并不是所有内容都经过了测试，而

且由于我们越来越依赖于尖端的编译器特性，因此系统的默认编译器可能存在错误的风险无法忽视。我

们已经尽力测试并拒绝在cmake中使用已知存在问题的版本，但我们强烈建议你自己运行这些测试。整  
个测试只需要几分钟，正常完成之后你就可以确信自己安装的程序工作正常。

运行检测的最简单方法是构建GROMACS时使用\-DREGRESSIONTEST\_DOWNLOAD，然后运行 make  
check。GROMACS会自动下载并运行测试。或者，你可以下载并解压 GROMACS回归测试  
压缩包http://gerrit\.gromacs\.org/download/regressiontests\-2019\.6\.tar\.gz，并使用 cmake 高级选项  
REGRESSIONTEST\_PATH 来指定解压后的路径，然后使用它进行测试。如果以上方法都不可行，请  
继续阅读。

回归测试也可以从官方网站 download↪\.\./download\.html 处下载。下载后，解压，按照前面所述的做法  
source GMXRC，然后在回归测试目录中运行\./gmxtest\.pl all。如果执行脚本时没有提供选项，脚本  
会给出可以使用的更多选项（例如，使用double选项可以测试双精度版本，或者使用\-only expanded  
选项只运行名称匹配expanded的那些测试）。

希望你能得到所有测试都已通过的报告。如果有个别测试失败，这可能预示着编译器存在错误，  
或者用于比较的容差太小了。还要检查脚本给出的输出文件，如果错误看起来是真实的，请试着  
换用不同的或更新的编译器。如果回归测试无法通过，你可以尝试到GROMACS用户论坛↪https:  
//gromacs\.bioexcel\.eu/c/gromacs\-user\-forum提问，但你应该给出所用硬件的详细描述，以及 gmx mdrun \-version  
的输出（其中的标题中含有一些有价值的诊断信息）。

##### 非标准后缀

如果gmx程序的后缀没有按照标准方式添加，那么可以使用 \./gmxtest\.pl \-suffix选项为测试机器  
指定所用的后缀。你可以使用\./gmxtest\.pl \-double来测试双精度版本。你可以使用 \./gmxtest\.pl  
\-crosscompiling来避免测试工具检查程序是否可以运行。如果运行MPI程序的命令名称为srun，那  
么可以使用\./gmxtest\.pl \-mpirun srun。

##### 运行启用 MPI 的测试

如果设置了GMX\_MPI=ON，make check的目标也可以运行integration\-style测试，它们可以用MPI运  
行。要将这些工作与各种可能的MPI库一起使用，你可能需要设置CMake变量MPIEXEC，MPIEXEC\_\-  
NUMPROC\_FLAG，MPIEXEC\_PREFLAGS 和 MPIEXEC\_POSTFLAGS，这样 mdrun\-mpi\-test\_mpi 可以通过  
shell命令在多个队列上运行

$\{ MPIEXEC \}$\{ MPIEXEC\_NUMPROC\_FLAG \}$\{ NUMPROC \}$\{ MPIEXEC\_PREFLAGS \} \*\*  
mdrun\-mpi\-test\_mpi $\{ MPIEXEC\_POSTFLAGS \} \-otherflags

SLURM的一个典型例子是

cmake\.\.\-DGMX\_MPI=on \-DMPIEXEC=srun\-DMPIEXEC\_NUMPROC\_FLAG=\-n \*\*  
\-DMPIEXEC\_PREFLAGS=\-DMPIEXEC\_POSTFLAGS=

#### 2\.3\.6 测试 GROMACS 的性能

我们正在开发一套基准测试系统，用以测试GROMACS的性能。在此之前，我们建议你试试一些不同

的并行化选项，并尝试使用诸如gmx tune\_pme之类的工具。

#### 2\.3\.7 遇到了困难

#### 并不是只有你才会遇到\-编译安装可能是一项复杂的任务\!如果在安装GROMACS时遇到问题，那么

##### 你可以在许多地方找到帮助。建议你按照以下步骤查找解决方案：

##### 1\.再次阅读安装说明，记下你已经正确执行的每个步骤。

2\.在GROMACS 网站↪http://www\.gromacs\.org 和用户论坛↪https://gromacs\.bioexcel\.eu/c/gromacs\-user\-forum/5中搜

索有关错误的信息。将site:https://gromacs\.bioexcel\.eu/c/gromacs\-user\-forum/5添加到

Google搜索文本中有助于过滤，查询到更好的结果。检查位于 https://mailman\-1\.sys\.kth\.

se/pipermail/gromacs\.org\_gmx\-users的GROMACS用户电子邮件列表存档↪https://mailman\-1\.sys\.

kth\.se/pipermail/gromacs\.org\_gmx\-users也是一个不错的主意\.

3\.使用Google等搜索引擎搜索互联网。

4\.到用户论坛↪https://gromacs\.bioexcel\.eu/c/gromacs\-user\-forum/5寻求帮助。一定要给出完整的描述，你已经做

了什么，为什么你认为它没起作用。提供要安装的系统的详细信息。复制并粘贴你所用的命令行，

以及你认为的可能有关的输出–当然是从出问题的第一个指示开始。特别是，请试着至少给出

mdrun日志文件中的开头部分，最好是整个文件。那些可能自愿帮助你的人没有时间和你互动，详

细询问后续问题，因此如果你提供了尽可能多的信息，问题就会尽快得到解决。高质量的错误报告

往往会得到快速，高质量的回答。

### 2\.4 针对某些平台的特别说明

#### 2\.4\.1 Windows 上的构建

在Windows上使用本机编译器进行构建方法与Unix非常相似，因此请先阅读上面的内容。然后，下载  
并解压GROMACS源码档案。创建一个文件夹，以便在其中执行GROMACS的源外构建。例如，将其  
放在从源代码档案解压出的文件夹中，并命名为build\-gromacs。  
对于CMake，你既可以使用Windows上提供的图形用户界面，也可以使用命令行shell，做法与上述  
Unix的类似。如果你从IDE（例如Microsoft Visual Studio）中打开一个shell，它会为你配置好环境，  
但你可能需要进行调整，以得到 32 位或 64 位构建环境。后者提供的可执行文件速度最快。如果使用  
普通的Windows命令shell，那么你需要自己设置环境来查找编译器和库，或者运行MSVC提供的  
vcvarsall\.bat批处理脚本（类似Unix下的bash脚本）。  
使用图形用户界面，程序会询问你在初始配置阶段使用哪种编译器，如果使用命令行，可以使用类似  
Unix的方式来设置它们。  
不幸的是，\-DGMX\_BUILD\_OWN\_FFTW=ON（参见使用 FFTW ↪ 10 ）在Windows下无法使用，因为FFTW  
不支持在Windows下构建。你可以通过其他方式构建FFTW（例如MinGW），或使用内置的fftpack  
（可能很慢）或使用 MKL ↪ 11 。

构建时，你可以将生成的解决方案文件加载到例如Visual Studio，或使用cmake \-\-build命令行，以

便使用正确的工具。

#### 2\.4\.2 Cray 上的构建

在现代Cray机器上GROMACS构建大多是开箱即用的，但你可能需要设置 \-DGMX\_BUILD\_SHARED\_\-  
EXE=off以便使用静态二进制文件，并且在编译FFTW时可能需要将F77环境变量设置为ftn。ARM  
ThunderX2 Cray XC50机器的不同之处仅在于推荐的编译器是ARM HPC编译器（armclang）。

#### 2\.4\.3 Solaris 上的构建

内置于GROMACS的处理器检测流程无法在Solaris上使用，因此强烈建议你构建GROMACS时使  
用\-DGMX\_HWLOC=on，并确保hwloc头文件和库的路径包含在CMAKE\_PREFIX\_PATH中。建议至少使用  
1\.11\.8版本的hwloc。

#### 2\.4\.4 Intel Xeon Phi

支持托管或自托管的Xeon Phi处理器。基于Knighs Landing的Xeon Phi处理器的行为类似于标准  
的x86节点，但支持特殊的SIMD指令集。对这类节点进行交叉编译时，请使用AVX\_512\_KNLSIMD。  
Knights Landing处理器支持所谓的“集群模式”这种模式允许重新配置内存子系统以降低延迟。使用  
quadrant或SNC群集模式可以提高GROMACS的性能。需要注意的是要正确地关联线程。特别是，  
MPI进程的线程不应跨集群和NUMA边界。除主DRAM内存外，Knights Landing还有一个高带宽的  
堆栈内存，称为MCDRAM。使用它可以提高性能，前提是确保 mdrun完全在这个内存中运行；为此，  
建议将MCDRAM配置为“Flat模式”，并将mdrun绑定到适当的NUMA节点（例如对quadrant集  
群模式使用numactl \-\-membind 1）。

## 第 3 章用户指南

### 3\.1 影响 GROMACS 用户的已知问题

#### 3\.1\.1 无法使用 CUDA 11\.3 进行编译

由于nvcc编译器中的一个错误，目前无法使用11\.3版本的CUDA编译器编译支持NVIDIA GPU的  
GROMACS。我们建议使用CUDA 11\.4或更新版本。

Issue 4037↪https://gitlab\.com/gromacs/gromacs/\-/issues/4037

#### 3\.1\.2 deform 选项不适合 flow

deform选项目前可以缩放坐标，但对于flow来说，变形只能通过改变周期向量来驱动。此外，当粒子  
被周期向量移位时，粒子的速度也需要修正。因此，deform选项目前只适用于缓慢变形的体系。

Issue 4607↪https://gitlab\.com/gromacs/gromacs/\-/issues/4607

#### 3\.1\.3 LevelZero 后端使用 oneAPI 时 SYCL 构建不稳定

使用LevelZero后端时，不同版本的Intel oneAPI存在多个问题。

在很多情况下，它能正常运行，如果出现故障，也会很明显（崩溃或挂起），因此可以放心使用。

对大多数情况，我们建议在Intel GPU上运行GROMACS的SYCL构建时使用OpenCL后端（默认）。

Issue 4219↪https://gitlab\.com/gromacs/gromacs/\-/issues/4219 Issue 4354↪https://gitlab\.com/gromacs/gromacs/\-/issues/4354

#### 3\.1\.4 在 Ubuntu 22\.04 上无法使用 CUDA 11\.5\-11\.6 和 GCC 11 进行构建

nvcc工具链11\.5\.0\-11\.6\.1版本中存在一个错误,导致无法使用Ubuntu 22\.04随带的GCC 11\.2构建最  
新的GROMACS。我们建议用户要么使用其他版本的GCC（在撰写本文时，有报告9\.x或10\.x可以正  
常工作），要么手动将nvcc工具链更新至11\.6\.2或更新版本。

据观察，一些GCC 11\.2库的非Ubuntu安装版本也能正常运行。

如果使用了不兼容的组合，在构建过程中CMake或之后会出现错误。

Issue 4574↪https://gitlab\.com/gromacs/gromacs/\-/issues/4574

#### 3\.1\.5 NVIDIA RTX 40xx 系列 GPU 联用 CUDA 11\.7 或更早版本时出现 FFT 错误

cuFFT库从11\.8版开始才完全支持RTX 40xx GPU。如果你使用旧版本的CUDA，那么在此类GPU  
上使用PME运行模拟时，可能会遇到 cufftPlanMany R2C plan failure错误。要解决这个问题，请  
升级到CUDA 11\.8或12\.x。

Issue 4759↪https://gitlab\.com/gromacs/gromacs/\-/issues/4759

#### 3\.1\.6 在未安装 CUDA 驱动程序的节点上进行构建时，基于 cuFFTMp 的 PME 分解

#### 构建在 NVHPC SDK 23\.3\+ 下坏掉

从cuFFTMp版本11\.0\.5 开始，它依赖于NVSHMEM，而NVSHMEM版本依赖于libnvshmem/\_\-  
host\.so。这个 cuFFTMp↪https://docs\.nvidia\.com/hpc\-sdk/cufftmp/release\_notes\.html\#new\-features 版本从NVHPC SDK  
23\.3\+开始发布。

要使用cuFFTMp 11\.0\.5及更高版本进行构建，必须明确链接到libnvidia\-ml\.so 和libcuda\.so库  
或这些库的存根版本。

要解决这个构建问题，请参考 cufftmp 部分。

Issue 4886↪https://gitlab\.com/gromacs/gromacs/\-/issues/4886

#### 3\.1\.7 使用 ROCm Clang 时出现“ Cannot find a working standard library ”错误

有些Clang安装未包含兼容的C\+\+标准库。在这种情况下，你可能需要安装 g\+\+并设置 \-DGMX\_\-  
GPLUSGPLUS\_PATH=/path/to/bin/g\+\+以便CMake能够使用它。

在Ubuntu 22\.04上，安装GCC 12标准库（使用sudo apt install libstdc\+\+\-12\-dev）后,即使不  
设置\-DGMX\_GPLUSGPLUS\_PATH通常也能够正常工作也。

Issue 4679↪https://gitlab\.com/gromacs/gromacs/\-/issues/4679

#### 3\.1\.8 在 Intel Gen9 GPU 上 Ryckaert\-Bell 二面角势能计算不精确

在SYCL/oneAPI构建中，当成键力卸载到Intel Gen9 GPU（HD Graphics 5xx至7xx系列；Skylake  
至Gemini Lake）上时，Ryckaert\-Bell势的计算不精确。这不太可能导致错误的结果，但我们仍建议在  
Gen9 Intel集成GPU上运行时禁用列表力的卸载（\-bonded cpu），特别是因为卸载不太可能在此类设  
备上提供明显的性能优势。

Issue 4686↪https://gitlab\.com/gromacs/gromacs/\-/issues/4686

#### 3\.1\.9 扩展系综无法正确地记录检查点

在遗留下的模拟器中，由于实现上的缺陷，出现在检查点步骤上,成功的扩展系综MC步骤并没有记录

在检查点中。如果使用该检查点重新启动模拟，那么之后的行为不一定正确也不具有可重复性。因此，

遗留模拟器禁用了扩展系综模拟的检查点功能。

##### 模块化模拟器中的扩展系综的检查点功能工作正常。

要解决这个问题，要么避免使用\-update gpu（这样它就会使用不存在错误的模块化模拟器路径），要  
么使用旧版本的GROMACS（它确实会进行有错误的检查点记录），要么避免在受影响的情况下从检查  
点重新启动。

Issue 4629↪https://gitlab\.com/gromacs/gromacs/\-/issues/4629

#### 3\.1\.10 POWER9 架构下使用 GCC 12 进行编译

##### 在POWER9架构下使用GCC 12\.2和12\.3编译后，有多个单元测试失败。其他GCC 12和更新版本

##### 也可能会受到影响。

Issue 4823↪https://gitlab\.com/gromacs/gromacs/\-/issues/4823

### 3\.2 入门

#### 设置环境

要检查你是否可以使用GROMACS软件，请输入以下命令：

gmx\-version

此命令应打印出安装的GROMACS的版本信息。如果返回的是

gmx: command not found\.

那么你必须确认GROMACS的安装位置。默认情况下，GROMACS的二进制应用程序位/usr/local/  
gromacs/bin。但是，你可以向机器的系统管理员咨询更多信息，然后按照安装后使用 GROMACS ↪ 24  
中的建议进行操作。

重要文件

你会在教程中遇到许多GROMACS文件类型，以下是一些最重要的文件类型的简要说明。

分子拓扑文件（ \.top ）

分子拓扑文件通常由 gmx pdb2gmx ↪ 297 程序生成。 gmx pdb2gmx ↪ 297 程序可以将任何多肽或蛋白质  
的 pdb ↪ 614 结构文件转换为分子拓扑文件。拓扑文件完整地描述了多肽或蛋白质中的所有相互作用。

拓扑的 \#include 文件机制

当在 top ↪ 617 文件中构建系统拓扑以便用于grompp时，GROMACS使用了所谓的C预处理器的内置版  
本cpp（在GROMACS 3中，它实际上就是cpp）。cpp将下面的行

\#include "ions\.itp"

解读为，在当前目录，GMXLIB 环境变量指定的GROMACSshare/top目录，以及 mdp ↪ 612 文件中运  
行参数↪ 123 的\-I 选项指定的任何目录中查找指定的文件。如果无法找到指定的文件，会给出警告信  
息。（注意，当指定目录名称时，应该使用Unix样式的正斜杠/，而不是Windows式的反斜杠\\作为  
分隔符。）找到文件后，程序会将文件中的内容精确地放在相应的位置，就像你自己使用复制和粘贴操作  
将包含文件的内容放在主文件中一样。注意，你不应该自己进行复制粘贴，因为包含文件机制的主要目  
的是重用以前的文件，这样将来修改更容易，也可以防止输入错误。

此外，cpp将如下代码：

\#ifdef POSRES\_WATER  
; Position restraint for each water oxygen  
\[ position\_restraints \]  
; i funct fcx fcy fcz  
1 1 1000 1000 1000  
\#endif

解读为，测试是否定义了预处理器变量POSRES\_WATER（即if defined）。这可以通过几种方法完成，  
在 top ↪ 617 文件（或其\#include的文件）的前面指定\#define POSRES\_WATER，为include运行参数  
的\-D 选项指定类似变量，或在cpp命令行上指定类似选项。\-D 选项的功能借用了cpp中的类似用  
法。\-D后面的字符串必须完全匹配；使用 \-DPOSRES不会触发\#ifdef POSRE或 \#ifdef DPOSRES。  
使用这种机制，可以通过更改 mdp ↪ 612 文件来选择是否对溶剂施加位置限制，而无须修改 top ↪ 617 文件。  
注意，预处理器变量与shell环境变量不同。

分子结构文件（ \.gro ， \.pdb ）

当使用 gmx pdb2gmx ↪ 297 程序生成分子拓扑时，同时会将结构文件（ pdb ↪ 614 文件）转换为GROMOS结  
构文件（ gro ↪ 610 文件）。 pdb ↪ 614 文件与gromos文件的主要区别在于其格式，此外 gro ↪ 610 文件还可以包  
含速度。但是，如果不需要速度，你可以在所有程序中都使用 pdb ↪ 614 文件。要将多肽放置到盒子中并在  
其周围填充溶剂分子，可使用 gmx solvate ↪ 328 程序。首先要使用 gmx editconf ↪ 231 程序在分子周围定义一  
个适当大小的盒子。 gmx solvate ↪ 328 可以将溶质分子（多肽）放入任何溶剂中（在这种情况下，溶剂是  
水）。 gmx solvate ↪ 328 会输出一个gromos结构文件，包含溶剂化的多肽。 gmx solvate ↪ 328 程序也可以修  
改分子拓扑文件（由 gmx pdb2gmx ↪ 297 生成），将溶剂添加到拓扑中。

分子动力学参数文件（ \.mdp ）

分子动力学参数（ mdp ↪ 612 ，Molecular Dynamics Parameter）文件包含了与分子动力学模拟本身有关的  
所有信息，如时间步长，积分步数，温度，压力等。得到这种文件的最简单方法是修改示例 mdp ↪ 612 文  
件。这里有一份示例 mdp 文件↪ 612 。

索引文件（ \.ndx ）

有时你可能需要一个索引文件来指定受影响的原子组（如温度耦合，加速度，冻结）。通常情况下，使用  
默认的索引组就够了，因此在本示例中，我们不考虑使用索引文件。

运行输入文件（ \.tpr ）

下一步是将分子结构（ gro ↪ 610 文件），拓扑（ top ↪ 617 文件），MD参数（ mdp ↪ 612 文件）和（可选的）索  
引文件（ ndx ↪ 613 ）组合起来生成一个运行输入文件（扩展名为 tpr ↪ 619 ）。此文件包含了GROMACS启动  
模拟所需的全部信息。 gmx grompp ↪ 252 程序会处理所有的输入文件并生成运行输入 tpr ↪ 619 文件。

轨迹文件（ \.trr ， \.tng 或 \.xtc ）

一旦准备好了运行输入文件，我们就可以开始进行模拟了。启动模拟的程序为 gmx mdrun ↪ 276 。通常情况  
下，启动模拟时 gmx mdrun ↪ 276 只需要一个运行输入文件（ tpr ↪ 619 文件）。 gmx mdrun ↪ 276 的典型输出文  
件是轨迹文件（ trr ↪ 619 文件），日志文件（ log ↪ 611 文件），可能还有检查点文件（ cpt ↪ 608 文件）。

#### 教程资料

有一些第三方教程↪http://www\.mdtutorials\.com/gmx/涵盖了使用GROMACS的各个方面。更多信息可参见简  
短的操作指南↪ 97 章节。

### 3\.3 系统准备

##### 可以使用多种方法来准备模拟系统，并用于GROMACS。作法往往因所考虑的科学问题的类型或所涉及

##### 的模型物理的不同而有所不同。蛋白质\-配体原子级别的自由能模拟可能需要多个状态的拓扑，而粗粒化

##### 模拟可能需要处理默认设置以保证系统具有合适的高密度。

#### 3\.3\.1 需要考虑的步骤

下面的一般性指导有助于进行一次成功的模拟。其中的具体步骤和过程可能取决于研究内容，对于某些

类型的模拟，某些阶段是可选的。

1\.明确地确定要通过模拟进行研究的感兴趣的性质或现象。在弄清楚这一点之前，不要继续下去\!不

要运行模拟，然后再设法弄清楚如何使用它来测试自己的假说，因为模拟可能不合适，或者没有保

存所需的信息。

2\.选择合适的工具，以便能够执行模拟并观察感兴趣的性质或现象。阅读并熟悉其他研究人员关于

类似系统的研究论文非常重要。工具的选择包括：

• 用于执行模拟的软件（考虑可用的力场可能会影响此决定）

• 力场描述了系统内的粒子如何相互作用。选择一个适合要研究的系统以及感兴趣的性质或现

象的力场。这是一个非常重要的步骤，而且并不简单\!现在就要考虑如何分析模拟数据以观测

感兴趣的性质或现象。

3\.对系统中要包括的每类分子，获取或生成其初始坐标文件。有许多不同的软件包可以构建分子结

构，并将它们组装成合适的构型。

4\.根据需要将分子置于坐标文件中，生成系统的原始初始结构。分子可以特殊地放置或随机

排列。处理时，可以使用一些非GROMACS的工具；GROMACS自带的 gmx solvate ↪ 328 ， gmx

insert\-molecules ↪ 264 和 gmx genconf ↪ 247 也能够解决常见的问题。

5\.获取或生成系统的拓扑文件，（例如）可以使用 gmx pdb2gmx ↪ 297 ， gmx x2top ↪ 361 ，SwissParam↪http:

//swissparam\.ch/（CHARMM力场），PRODRG↪http://davapc1\.bioch\.dundee\.ac\.uk/cgi\-bin/prodrg（GROMOS96

43A1力场），Automated Topology Builder↪https://atb\.uq\.edu\.au/（GROMOS96 53A6力场），MK\-

TOP↪http://www\.aribeiro\.net\.br/mktop（OPLS/AA力场），或你自己喜欢的文本编辑器以及GRO\-

MACS 参考手册第 5 章↪ 524 的说明。对于 AMBER 力场，可以使用 antechamber↪https:

//ambermd\.org/antechamber/antechamber\.html 或 acpype↪https://github\.com/alanwilter/acpype。

6\.指定一个模拟盒子（例如使用 gmx editconf ↪ 231 ），其大小取决于你最终需要的密度，并向其中填

充溶剂（例如使用 gmx solvate ↪ 328 ），再添加需要的抗衡离子以维持系统电中性（例如，使用 gmx

grompp ↪ 252 和 gmx insert\-molecules ↪ 264 ）。在这些步骤中，你可能需要编辑拓扑文件以保证它与坐

标文件一致。

7\.对系统进行能量最小化（使用 gmx grompp ↪ 252 和 gmx mdrun ↪ 276 ）。这样可以修正在系统生成过程

中引入的结构异常。直接使用起始结构进行模拟可能导致成品模拟崩溃。在引入溶剂分子（或脂质

双层或其他任何物种）之前，可能还需要在真空中对溶质结构进行能量最小化。你应该考虑使用柔

性水模型，而不使用键约束或冻结组。你还应该仔细评估下是否需要使用位置限制和/或距离限制。

8\.为平衡模拟选择合适的模拟参数（在 mdp ↪ 612 文件中定义）。你选择的模拟参数需要与力场导出参

数的方式一致。你可能需要先使用NVT系综进行模拟，并对溶剂和/或溶质施加位置限制以获得

基本正确的温度，然后弛豫到NPT系综，以保证密度正常（应该首先使用Berendsen方法控压，

密度稳定后再换用能够产生正确系综的控压器），最后（如果需要的话）进行成品系综的模拟（例

如NVT，NVE）。如果你的系统出现爆破↪ 60 问题，请考虑其页面给出的建议，例如，对溶质施加

位置限制，或不使用键约束，或使用更小的积分时间步长，进行几个较缓慢的加热阶段。

9\.运行足够长时间的预平衡模拟，使得系统在目标系综中充分弛豫，以便开始运行成品模拟（使

用 gmx grompp ↪ 252 和 gmx mdrun ↪ 276 ，然后 gmx energy ↪ 237 和可视化软件 Software ）。

10\.为成品模拟选择合适的模拟参数（在 mdp ↪ 612 文件中定义）。特别注意，不要重新产生速度。模拟

参数的设置仍然需要考虑力场的参数化方式，还要考虑测量感兴趣的性质或现象的方式。

11\.运行成品模拟足够长时间，产生足够详细的数据以研究感兴趣的性质或现象（使用 gmx grompp ↪ 252

和 gmx mdrun ↪ 276 ）。

12\.对得到的轨迹和数据文件进行分析或可视化，获得感兴趣的性质或现象的信息。

有关副本交换模拟的步骤请参见REMD部分。

#### 3\.3\.2 技巧和窍门

##### 数据库文件

GROMACS安装目录下的share/top目录中包含许多扩展名为\.dat的纯文本帮助文件。一些命令行  
工具（参见命令行参考↪ 170 ）引用了这些文件，每个工具都会记录它使用的文件以及它们的使用方式。

如果你需要修改这些文件（例如，要在vdwradii\.dat中引入带有范德华半径的新原子类型），你可以  
将文件从安装目录复制到工作目录中，GROMACS工具会自动加载工作目录中的文件副本，而不加载标  
准目录中的文件。要取消所有的标准定义，可以在工作目录中使用空文件。

### 3\.4 管理长时间的模拟

分子模拟所需的时间通常会超出单个Unix命令行进程所允许的最大时间。因此，我们需要能够停止并  
重新启动模拟，停止和重启所得的结果应该和单次运行相同。当 gmx mdrun ↪ 276 停止时，会输出一个检  
查点文件，这个文件可用于重启模拟，就像没有中断一样。为此，检查点文件中保存了全精度的位置和  
速度，以及重启算法所需的状态信息，例如那些与外部热库耦合算法实现有关的信息。可以尝试使用，  
例如一个带有速度的 gro ↪ 610 文件进行重启。但由于 gro ↪ 610 文件的精度很低，并且所有耦合算法都无法保  
持其状态不变，因此这种重启不像正常的MD步骤那样连续。

在运行期间， gmx mdrun ↪ 276 也会定期输出这样的检查点文件。时间间隔由 gmx mdrun ↪ 276 的\-cpt选  
项指定。当 gmx mdrun ↪ 276 尝试输出连续的检查点文件时，它会首先在旧文件的名称后面加上\_prev，  
这样即使在输出新的检查点文件时出现了问题，也只会失去最近的模拟信息。

可以通过几种方式终止 gmx mdrun ↪ 276 的运行：

- 超过模拟步数 nsteps ↪ 125
- 用户发出终止信号（例如，在终端上使用Ctrl\-C）
- 作业调度程序在运行超时后发出终止信号
- gmx mdrun ↪ 276 检测到运行时间已经达到了\-maxh 指定的值（此选项可以配合作业调度程序，但  
如果作业可以挂起，则可能会出现问题）
- 某种灾难性的故障，如断电，磁盘已满或网络故障

要使用检查点文件重启模拟，可使用命令行，如

gmx mdrun\-cpi state

上面的命令指示mdrun使用检查点文件（默认名称为state\.cpt）。你可以使用\-cpo 选项为输出的  
检查点文件指定不同的名称，如果这样的话，以后使用此检查点文件时，必须为\-cpi选项指定相应的  
名称。你可以使用 gmx check ↪ 192 和 gmx dump ↪ 227 查看检查点文件的内容。

#### 3\.4\.1 追加到输出文件

默认情况下， gmx mdrun ↪ 276 的输出会追加到旧的输出文件中。如果前一部分模拟以常规方式结束，会  
删除日志文件末尾的性能数据，写入有关运行上下文的一些新信息，并继续进行模拟。否则，mdrun会  
将所有输出文件截断至检查点文件的最后输出时间，并从那里继续，就像模拟以常规方式停止在该检查  
点一样。

你可以使用\-noappend 选项指定不追加输出文件，这样会强制mdrun 将每个输出都写入到单独的文  
件，其名称包含一个\.partXXXX字符串用以说明文件中包含了哪些模拟部分。编号从零开始，并随模拟  
重启次数单调增加，但并不反映每一部分的模拟步数。 simulation\-part ↪ 125 选项可用于手动设置 gmx  
grompp ↪ 252 所用的这个数字，这在数据丢失时会用到，例如由于文件系统故障或用户错误而导致的数据  
丢失。

如果在mdrun写入之后修改或删除了任何输出文件，追加就会无效，因为检查点文件维护了每个文件的  
校验码，在再次写入之前会对其进行验证。在这种情况下，你必须还原文件，将其命名为检查点文件所  
需的名称，或者使用\-noappend选项继续运行。如果原来运行时使用了 \-deffnm，想要追加输出，那  
么继续运行时也必须使用\-deffnm。

#### 3\.4\.2 备份文件

你应该经常备份模拟文件。集群上的网络文件系统的配置可能或多或少有些保守，这会导致系统告知 gmx  
mdrun ↪ 276 检查点文件已经写入了磁盘，而实际上文件仍然在内存中，因此如果在此期间发生电源故障  
或磁盘错误，就无法更新检查点文件。Unix工具rsync可以定期将模拟输出复制到远程存储位置即使模  
拟正在运行也可以安全工作。如果文件系统不可靠，对提交到集群的作业的每一部分，保留其最终检查  
点文件的副本可能很有用。

#### 3\.4\.3 延长 \.tpr 文件的时间

如果 tpr ↪ 619 文件对应的模拟已经完成并且需要进行延长，可以使用 gmx convert\-tpr ↪ 203 工具来延长运行，  
例如：

gmx convert\-tpr\-s previous\.tpr\-extend timetoextendby\-onext\.tpr  
gmx mdrun\-snext\.tpr\-cpi state\.cpt

也可以使用\-until和\-nsteps选项来延长模拟时间。注意，原始的 mdp ↪ 612 文件可能产生了速度，但  
那是 gmx grompp ↪ 252 的一次性操作，任何其他工具都不会再次进行此操作。

#### 3\.4\.4 更改 mdp 选项以重新启动模拟

如果你希望更改模拟设置而不是模拟时间长度，那么你应该修改 mdp ↪ 612 文件或拓扑文件，然后使用

gmx grompp\-f possibly\-changed\.mdp\-p possibly\-changed\.top\-c original\.gro\-t state\.cpt\-o new\.  
↪tpr  
gmx mdrun\-s new\.tpr\-cpi state\.cpt

指示 gmx grompp ↪ 252 将检查点文件中的全精度坐标和速度复制到新的 tpr ↪ 619 文件中。你应该  
考虑 tinit ↪ 125 ， init\-step ↪ 125 ， nsteps ↪ 125 和 simulation\-part ↪ 125 选项的设置。通常不应该使  
用 gen\-vel ↪ 140 重新产生速度，并且通常选择 continuation ↪ 141 ，这样在第一个积分步骤前不会再重新  
施加约束。

#### 3\.4\.5 不存在检查点文件时重新启动模拟

##### 以前可以在没有检查点文件的情况下继续模拟。由于这种方法可能不可靠或导致不合理的结果，因此现

##### 在只允许使用检查点重新启动模拟。

#### 3\.4\.6 续跑是否精确?

##### 如果你的计算机具有无限精度，或者你手动积分时间离散的运动方程，那么精确的续跑会给出完全相同

##### 的结果。但实际计算机的精度有限，且MD具有混沌性，因此，即使只有一个数位不同，轨迹也会迅速

##### 发散。这些轨迹同样有效，但最终彼此间会有很大不同。使用检查点文件续跑，使用相同编译器编译的

##### 相同代码，并且在不使用GPU的情况下（参见下一节）使用相同数目的处理器在相同的计算机架构上

##### 进行续跑，会得到二进制相同的结果。但是，默认情况下，实际工作负载会根据观察到的执行时间在硬

##### 件之间进行平衡。这种轨迹原则上是不可重现的，特别是，分成多次运行完成的模拟与等价的单次运行

##### 所得的结果并不完全相同，但在任何意义上都无法确定哪一个更好。

#### 3\.4\.7 重现性

##### 以下因素会影响模拟的重现性，从而影响模拟输出：

##### • 双精度的重现性“更好”。

- 核的数目，因为累加力的顺序不同。例如，在浮点运算中，\(a\+b\)\+c不一定与a\+\(b\+c\)二进制相  
同。
- 处理器类型。即使相同的处理器系列，也可能存在细微差别。
- 编译时的优化级别。
- 运行时的优化。例如通常用于快速傅里叶变换的FFTW库在启动时会确定其算法的哪个版本最  
快，并将其用于其余的计算。由于速度估计并不是确定性的，因此结果可能会因运行而异。
- 随机数，例如用于生成速度的种子（在GROMACS的预处理阶段）。
- 代码中未初始化的变量（但它们本来不应该存在）
- 动态链接到不同版本的共享库（例如用于FFT的库）
- 动态负载均衡，由于粒子会根据经过的挂钟时间重新分配到处理器上，这可能导致\(a\+b\)\+c \!=  
a\+\(b\+c\)的问题，如前所述
- 仅用于PME的进程数（用于并行PME模拟）
- MPI归约通常无法保证操作顺序，因此浮点运算没有相关性，这意味着归约的结果取决于实际选  
择的顺序
- 在GPU上，进行诸如非键力之类的归约时求和顺序不确定，因此任何快速实现在设计上都是不可  
重现的。

重要的是，如果模拟不能完全重现，这是否是一个问题。答案既是肯定的，也是否定的。一般而言，重现  
性是科学的基石，因此它很重要。中心极限定理↪https://en\.wikipedia\.org/wiki/Central\_limit\_theorem 告诉我们，在  
无限长模拟的情况下，所有的可观测量都会收敛到它们的平衡值。GROMACS中的分子模拟遵循这个定  
理，因此，例如，系统的能量会收敛到一个有限的值，水分子的扩散系数会收敛到一个有限的值，等等。  
这意味着所有重要的可观察量，也就是你希望从模拟中获得的值，都是可重现的。然而，每条单独的轨  
迹都是不可重现的。

然而，在一些情况下，如果轨迹可以重现，也有好处。这些情况包括，开发人员正在进行调试，在轨迹  
中搜索罕见的事件，如果它发生了，你希望手动保存检查点文件，以便可以在不同条件下重启模拟，例  
如更频繁地输出模拟数据。

为了获得这种可重现的轨迹，查看上面的列表并消除可能的影响因素非常重要。此外，使用

gmx mdrun\-reprod

可以消除不可重现性的所有可能来源，即相同的可执行文件\+相同的硬件\+相同的共享库\+相同的运  
行输入文件\+相同的命令行参数会导致可重现的结果。

### 3\.5 常见问题（ FAQ ）

#### 3\.5\.1 有关 GROMACS 安装的问题

##### 1\.是否需要使用MPI编译所有实用程序?

除一个很少使用的程序（ pme\_error ↪ 300 ）之外，只有 mdrun ↪ 276 支持 MPI ↪ 9 并行。因此，在构建

主模拟引擎 mdrun ↪ 276 时，只要使用\-DGMX\_MPI=on选项进行编译↪ 13 即可。一般来说，在多节

点集群上运行时需要这样做，使用多模拟算法时也需要这样做。通常情况下，安装不带MPI的

GROMACS版本也会为用户提供方便。

2\.是否应该使用双精度编译?

通常，只需要使用默认的混合精度模式构建GROMACS即可。更多详细信息，请参阅参考手册↪ 469

第 2 节。有时，使用情况也可能取决于你的目标系统，应根据针对某些平台的特别说明↪ 26 来决定。

#### 3\.5\.2 有关系统准备和预处理的问题

1\.执行 gmx solvate ↪ 328 的时候需要溶剂分子的坐标文件↪ 606 ，哪里可以找到这些坐标文件?

合适的已平衡好的溶剂盒子的坐标文件↪ 606 可以在$GMXDIR/share/gromacs/top目录中找到。默

认情况下， solvate ↪ 328 会自动搜索该目录，例如使用\-cs spc216\.gro 作为参数时。用户可以按

照 solvate ↪ 328 手册页以及其他一些说明来准备其他溶剂盒子。注意，溶剂盒子需要合适的拓扑文件

才能用于 grompp ↪ 252 。一些力场含有需要的拓扑文件，可以在$GMXDIR/share/gromacs/top的相

应子目录中找到。

2\.如何避免 solvate ↪ 328 将水放置到不需要的位置?

在溶剂化蛋白质时，水分子的放置方法通常表现良好，但在设置膜或胶束模拟时，放置水

分子可能变得很困难。在这些情况下，水可能被放置到脂质的烷基链之间，导致后面的模拟

出现问题↪ 60 。你可以手动删除这些水分子（并修改拓扑↪ 617 文件中水分子类型的数目），或

者从 $GMXLIB 目录复制一份 vdwradii\.dat 文件到当前项目的工作目录。然后增加文件中

的原子范德华半径，这样可以减少插入到空隙中的水分子。建议的设置，例如在常见的 教

程↪http://www\.mdtutorials\.com/gmx/lysozyme/03\_solvate\.html 中使用0\.375而不是0\.15。

3\.如何在拓扑中对键/二面角进行多重定义?

除通常为残基定义的成键项之外，你可以添加其他成键项（例如定义一个特殊的配体时），方法是

在分子\[ moleculetype \]节段下的\[ bonds \]，\[ pairs \]，\[ angles \] 和\[ dihedrals \]

中添加相应的行，这些行的内容可以在 itp ↪ 611 文件或拓扑↪ 617 文件中找到。在计算势能时，这些额

外项会累加到势能中，而不会忽略以前的项对势能的贡献。因此，重复定义时要多加小心。还要记

住，这不适用于力场定义文件中\[ bondtypes \]，\[ angletypes \] 或\[ dihedraltypes \]节

段下的重复项，这些节段中的重复项会覆盖前面的值。

4\.必须要准备一个 gro ↪ 610 文件吗?

GROMACS将 gro ↪ 610 文件作为统一的结构文件↪ 606 格式，所有实用程序都可以读取这种格式。绝

大多数GROMACS例程也可以使用其他文件类型，例如 pdb ↪ 614 ，其限制是这些格式↪ 35 无法提供

速度。如果你需要一种精度更高的文本格式，可以使用 g96 ↪ 609 格式，程序也支持这种格式。

5\.如果已经通过其他方式得到了 itp ↪ 611 文件，是否还需要运行 pdb2gmx ↪ 297?

如果已经通过其他工具准备好了所有的 itp ↪ 611 和 top ↪ 617 文件，就不再需要准备额外的拓扑文件了。

可以使用的其他工具包括 CHARMM\-GUI↪http://www\.charmm\-gui\.org/，ATB（Automated Topology

Builder）↪https://atb\.uq\.edu\.au/，pmx↪http://pmx\.mpibpc\.mpg\.de/instructions\.html，以及 PRODRG↪http://davapc1\.

bioch\.dundee\.ac\.uk/cgi\-bin/prodrg。

6\.如何添加缺失的原子?

GROMACS不支持构建缺失的非氢原子的坐标。如果你的系统缺少某些原子，那你必须使用外部程

序添加缺失的原子，以避免缺失原子↪ 49 错误。可用的程序包括Chimera↪https://www\.cgl\.ucsf\.edu/chimera/，

以及Modeller↪https://salilab\.org/modeller/，Swiss PDB Viewer↪https://spdbv\.vital\-it\.ch/，Maestro↪https://www\.

schrodinger\.com/maestro。不要运行对原子缺失的系统进行模拟，除非你精确地知道为什么它会是稳定的。

7\.为什么我的系统的总电荷不是整数，它应该是整数啊?

浮点数↪ 69 无法以任意精度表示实数（更多信息可以参考 维基百科↪https://en\.wikipedia\.org/wiki/

Floating\-point\_arithmetic）。这意味着最终得到的总电荷与整数值可能存在微小差异，GROMACS

不会对这些值进行舍入。如果系统的总电荷与整数值相差较大，例如大于0\.01，这通常意味着准

备系统的过程中出了问题。

#### 3\.5\.3 有关模拟方法的问题

1\.是否应该将少量离子耦合到它们自己的温度耦合浴中?

不。你要考虑温度耦合组的最少数目，控温器↪ 58 对此有说明，更具体说明见不要做什么↪ 59 ，你还

要考虑所选恒温器的实现，见参考手册↪ 469 的说明。

2\.为什么我的grompp重启模拟时时间总是从零开始?

你可以将 tinit ↪ 125 和 init\-step ↪ 125 指定为不同的值。还可参考继续模拟一节的相关内

容:ref:Continuing simulations <gmx\-cont\-simulation>\.

3\.有约束的情况下为什么不能进行共轭梯度最小化?

共轭梯度能量最小化方法不能使用约束，参考手册↪ 469 对此有说明，一些补充信息见 维基百

科↪https://en\.wikipedia\.org/wiki/Conjugate\_gradient\_method。

4\.在能量最小化或模拟中，如何将原子保持在适当的位置?

可以使用freeze groups将原子组冻结在固定的位置（见参考手册↪ 469 ）。更常见的方法是使用位

置限制，对原子的移动施加惩罚。可以使用 genrestr ↪ 251 命令创建位置限制文件，以满足需要。

5\.如何为已完成的模拟延长模拟时间?

请参阅管理长时间的模拟↪ 38 一节。你可以准备一个新的 mdp ↪ 612 文件，或者使用 convert\-tpr ↪ 203 延

长原始 tpr ↪ 619 文件中的模拟时间。

6\.如何完成崩溃的模拟?

很容易读取检查点文件然后继续模拟,参考继续崩溃的模拟相关内容:ref:available <gmx\-cont\-

crash>\.

7\.如何进行恒pH模拟?

gmx\-howto\-cph doc target\.

这是一个很大的话题,首先你至少需要阅读简短说明, :ref:Constant pH How\-To <gmx\-howto\-cph>,

以及其中所提及的所有文献对问题有个大致的了解\.

8\.如何计算单点能?

最好的方法是使用 mdrun ↪ 276 的\-rerun 选项。参见重新运行模拟↪ 71 一节。

#### 3\.5\.4 参数化与力场

1\.我想模拟一个分子（蛋白质，DNA等），它与各种过渡金属离子，铁硫团簇或其他外来物种结合在

一起。力场X中不存在这些外来物种的参数。我该怎么办?

首先，你应该考虑一下， MD ↪ 62 实际上能否很好地描述你的系统（例如可以看一些 最近的文

献↪https://dx\.doi\.org/10\.1021%2Facs\.chemrev\.6b00440）。在不考虑原子极化率或QM处理的情况下，许多物种

是无法建模的。然后，你需要准备自己的参数集，并将新的残基添加到你选用的力场↪ 63 中。然后，

在继续进行模拟研究之前，你必须验证系统的运动是否符合物理。你还可以尝试构建一个更简单

的模型，不包含复杂的额外分子，只要它仍然能够代表实验室中正确的真实对象。

2\.能否将一个力场中的参数应用到另一个缺少参数的力场中?

不能。在一个给定力场↪ 63 中参数化的分子，当它们与参数化标准不同的其他分子相互作用时，其

行为可能不合理。如果你使用的力场中没有所需分子的参数，你必须根据所用力场的参数化方法

自己对分子进行参数化。

#### 3\.5\.5 分析与可视化

1\.如何可视化轨迹? gmx\-howto\-visualize doc target

有很多种程序可用于坐标的可视化,参考:ref:files and trajectories <gmx\-howto\-visualize>\.

2\.当观看轨迹时，为什么有时会看到一些不应该存在的键?

大多数可视化软件根据一组预先定义的距离来确定原子的成键状态。因此，它们显示的成键模式可

能与你在拓扑↪ 617 文件中定义的不同。只有拓扑文件中的成键信息最关键。如果软件读取了 tpr ↪ 619

文件，那么成键信息应该与你提供给 grompp ↪ 252 的拓扑中的一致。

3\.当使用PBC可视化模拟轨迹时，为什么会出现孔洞，或我的多肽为什么离开了模拟盒子?

这些孔洞和分子的移动只是分子穿过盒子边界并折叠↪ 57 的结果，对模拟结果没有影响，无须担心。

你可以使用 trjconv ↪ 343 命令修复可视化的显示问题，并准备用于分析的结构。

4\.为什么我的总模拟时间不是整数，它应该是整数啊?

由于计算模拟时间时使用了浮点运算↪ 69 ，所以可能存在舍入误差，但无关紧要。

### 3\.6 GROMACS 中的力场

#### 3\.6\.1 AMBER

AMBER↪http://ambermd\.org/（Assisted Model Building and Energy Refinement模型构建和能量细化辅助  
工具）既可以表示一套用于模拟生物分子的分子力学力场↪ 63 ，也可以表示一套分子模拟程序。

GROMACS原生支持以下AMBER力场：

AMBER94

• AMBER96

• AMBER99

• AMBER99SB

• AMBER99SB\-ILDN

• AMBER03

• AMBERGS

##### 有关力场的信息可以参考：

- AMBER Force Fields↪https://ambermd\.org/AmberModels\.php \- AMBER力场的背景信息
- AMBER Programs↪https://ambermd\.org/AmberTools\.php\- AMBER分子模拟程序包的信息
- ANTECHAMBER/GAFF↪http://ambermd\.org/antechamber/antechamber\.html \-通用AMBER力场（GAFF），  
用于提供与AMBER蛋白/核酸力场兼容的小分子的参数。这种力场既可以随AMBER一  
起使用，也可以通过antechamber 程序获得，antechamber 程序也可以单独分发。可以使用  
一些脚本将AMBER体系（例如使用GAFF的设置）转换到GROMACS（amb2gmx\.pl↪https:  
//github\.com/choderalab/mmtools/blob/master/converters/amb2gmx\.pl 或ACPYPE↪https://github\.com/alanwilter/acpype），但  
都需要先安装AmberTools↪https://ambermd\.org/AmberTools\.php才能使用它们。

#### 3\.6\.2 CHARMM

CHARMM↪http://www\.charmm\.org/（Chemistry at HARvard Macromolecular Mechanics哈佛大学分子力学  
化学）是一套力场和程序包，用于分子动力学↪ 62 模拟和分析。包括联合原子（CHARMM19）和全原子  
（CHARMM22，CHARMM27，CHARMM36）力场↪ 63 。CHARMM27力场已移植到GROMACS，并得  
到正式支持。可以从 MacKerell课题组↪http://mackerell\.umaryland\.edu/charmm\_ff\.shtml\#gromacs 获得CHARMM36  
的力场文件，该网站会定期发布GROMACS格式的最新CHARMM力场文件。  
要在GROMACS中使用CHARMM36，请在 mdp ↪ 612 文件中使用以下设置：

constraints=h\-bonds

cutoff\-scheme=Verlet

vdwtype=cutoff

vdw\-modifier=force\-switch

rlist=1\.2

rvdw=1\.2

rvdw\-switch=1\.0

coulombtype=PME

rcoulomb=1\.2

DispCorr=no

注意，色散校正应该用于脂质单层，但不能用于脂质双层。

还要注意，在脂质双层模拟中，切换距离是一个有争论的问题，它在某种程度上取决于脂质的性质。一

些研究发现切换距离0\.8\-1\.0 nm是合适的，另一些人认为0\.8\-1\.2 nm是最好的，还有一些人认为1\.0\-1\.2

nm最好。在开始模拟之前，提醒用户深入调查一下所选脂质力场的文献\!

#### 3\.6\.3 GROMOS

##### 警告 :

GROMOS力场参数化时,为双范围截断采用了物理上不正确的多重时间步长方案。当用于单范围

截断（或正确的Trotter多重时间步长方案）时，物理性质,如密度,可能会与预期值不同。由于一

些研究人员正在积极地使用现代积分器验证GROMOS，因此我们尚未移除GROMOS力场，但你

应该注意这些问题，并在继续使用之前检查体系中的分子是否会受影响。更多信息请参见 GitLab

Issue 2884↪https://gitlab\.com/gromacs/gromacs/\-/issues/2884 。关于我们决定移除物理上不正确算法的更详细解

释，请参见 DOI:10\.26434/chemrxiv\.11474583\.v1↪https://doi\.org/10\.26434/chemrxiv\.11474583\.v1 。

GROMOS↪ttps://www\.igc\.ethz\.ch/gromos\.html 是一个通用的分子动力学计算模拟程序包，用于研究生物分子系  
统。它还包含自己的力场，涵盖蛋白质，核酸，糖等。它能够用于各种化学和物理系统，从玻璃和液晶，  
到聚合物和晶体，以及生物分子溶液。

GROMACS支持GROMOS力场43a1，43a2，45a3，53a5，53a6和54a7发布中提供的所有参数。  
GROMOS力场是联合原子力场↪ 63 ，即没有显式的脂肪族（非极性）氢。

GROMOS 53a6 \- GROMACS格式\(J\. Comput\. Chem\. 2004 vol\. 25 \(13\): 1656\-1676\)\.

GROMOS 53a5 \- GROMACS格式\(J\. Comput\. Chem\. 2004 vol\. 25 \(13\): 1656\-1676\)\.

GROMOS 43a1p \- 43a1的改进版，包含了SEP（磷酸丝氨酸），TPO（磷酸苏氨酸）和PTR（磷  
酸酪氨酸）（所有PO42\-形式），以及SEPH，TPOH，PTRH（PO4H\-形式）\.

#### 3\.6\.4 OPLS

OPLS（Optimized Potential for Liquid Simulations用于液体模拟的优化势）是由William L\. Jorgensen  
教授发展的力场，用于凝聚相模拟，最新版本为 OPLS\-AA/M↪http://zarbi\.chem\.yale\.edu/oplsaam\.html。

这些力场的标准实现是 Jorgensen组↪http://zarbi\.chem\.yale\.edu/software\.html开发的 BOSS 和 MCPRO 程序。

由于没有权威网页可供参考，建议用户查阅 联合原子（OPLS\-UA）↪https://doi\.org/10\.1021%2Fja00214a001 和  
全原子（OPLS\-AA）↪https://doi\.org/10\.1021%2Fja9621760 力场的原始文献，以及Jorgensen课题组的 网  
站↪http://zarbi\.chem\.yale\.edu/。

### 3\.7 非键截断方案

GROMACS 2019\.6中的默认截断方案基于经典的缓冲Verlet列表。在现代CPU和加速器上这些实现  
非常高效，并且几乎支持GROMACS中使用的所有算法。

在4\.6版本之前，GROMACS始终使用基于粒子组的配对列表。这些粒子组最初是电荷组，普通截断静  
电算法需要它们。使用PME（或带缓冲区的反应场）时，不再需要电荷组（在Verlet方案中会忽略电  
荷组）。在GROMACS 4\.6及更高版本中，基于组的截断方案仍然可以使用，但自 5\.0 版本起已被废  
弃。它仍然可以使用主要是为了向后兼容，以支持那些尚未进行转换的算法，此外，在少数情况下，对  
以水为主的生物分子系统进行模拟时，使用这种方法可能更快。

如果不使用PME，组截断方案通常应该与缓冲配对列表一起使用，以帮助避免假象。然而，可以实现这  
一点的组方案内核要比无缓冲的组方案内核或缓冲的Verlet方案内核慢得多。强烈建议使用Verlet方

案进行各种模拟，因为更容易正确运行，也更快。特别是，GPU加速只能使用Verlet方案。

Verlet方案使用了具有精确截断值的合适的缓冲列表。缓冲区的大小由 verlet\-buffer\-tolerance ↪ 129

选项指定，允许一定程度的漂移。通过减去截断处的值，LJ和库仑势都偏移到了零。这就保证了能量是

力的积分。但我们仍然建议在截断处保留小的力，因此可以使用PME或具有无穷大介电常数的反应场。

#### 3\.7\.2 性能

##### 组截断方案的性能在很大程度上取决于系统的组成和缓冲的使用。对涉及水的相互作用，可以使用优化

##### 的内核，因此任何含有大量水的模拟都可以运行得非常快。但是，如果你需要缓冲正确的相互作用，那

##### 么需要添加一个考虑电荷组大小和扩散的缓冲区，并在每个时间步根据截断长度检查每个相互作用。这

会导致模拟速度大大降低。对于使用新非键内核的Verlet方案，其性能与系统组成无关，并且始终与缓  
冲配对列表一起运行。通常，缓冲区大小为截断值的0%到10%，因此可以通过减少或移除缓冲区来提  
高一些性能，但这对模拟质量而言可能不是一个好的折衷方案。  
下表展示了大多数相关设置的性能比较。除非使用联合原子力场，否则任何原子模型的性能都与tips3p  
（氢原子具有LJ相互作用）相当。模拟水中蛋白质的性能介于tip3p和tips3p之间。组方案针对涉及

##### 水的相互作用进行了优化，这类相互作用只涉及单个电荷组，包含一个具有LJ相互作用的粒子和 2 个

##### 或 3 个不具有LJ相互作用的粒子。这种用于水的内核，其速度大约是具有LJ和/或无电荷组的相近系

统的两倍。除少于一半的粒子具有LJ时只计算LJ相互作用的一半外，Verlet截断方案的实现没有针对  
特定相互作用进行其他优化。对于水盒子中分子的模拟，Verlet方案对更多核数的标度行为比组方案好，  
因为它的负载更均衡。在最新的Intel CPU上，Verlet方案的绝对性能超过组方案，甚至对于纯水系统  
也是如此。

表：GROMACS中不同非键设置下各种水系统的模拟性能，单位为ns/天，使用了 8 线程MPI进程（组  
方案）或 8 个OpenMP线程（Verlet方案）。粒子数 3000 ，截断值1\.0 nm，PME格点0\.11 nm，dt=2  
fs，Intel Core i7 2600\(AVX\)，3\.4 GHz \+ Nvidia GTX660Ti

系统 组方案，无缓冲 组方案，缓冲 Verlet，缓冲 Verlet，缓冲，GPU

tip3p，电荷组 208 116 170 450

tips3p，电荷组 129 63 162 450

tips3p，无电荷组 104 75 162 450

#### 3\.7\.3 如何使用 Verlet 方案

cutoff\-scheme ↪ 128 选项默认会启用Verlet方案。 mdp ↪ 612 选项 verlet\-buffer\-tolerance ↪ 129 的值会  
添加一个配对列表缓冲区，其大小针对给定的能量漂移进行调整（以kJ/mol/ns/particle为单位）。有  
效漂移通常要低得多，因为 gmx grompp ↪ 252 假定粒子速度不变。（注意，对于使用单精度的常规原子模  
拟，约束导致的每个粒子的漂移大约为0\.0001 kJ/mol/ns，所以漂移降低得更多没有意义。）有关选择缓  
冲区大小的详细信息见后文以及参考手册↪ 469 。

对于等能量（NVE）模拟，会根据温度推断缓冲区大小，温度则根据速度计算得到（速度来自随机生成  
或输入构型文件）。或者，可以将 verlet\-buffer\-tolerance ↪ 129 设置为\-1，并通过将 rlist ↪ 130 指定为  
同时大于 rcoulomb ↪ 132 和 rvdw ↪ 133 的值来手动设置缓冲区。获得合理缓冲区大小的最简单方法是，使  
用NVT mdp文件，将目标温度设置为NVE模拟要使用的值，然后将 gmx grompp ↪ 252 给出的缓冲区大  
小用于NVE的 mdp ↪ 612 文件。

当使用GPU时， gmx mdrun ↪ 276 会自动增加 nstlist ↪ 128 的值，通常会增加到 20 或更大；同时也会增  
加 rlist ↪ 130 以保证能量漂移低于预期目标。使用GPU运行 gmx mdrun ↪ 276 的更多信息见这里↪ 88 。

#### 3\.7\.4 更多信息

有关Verlet截断方案和MxN内核的算法，实现细节的更多信息，以及详细的性能分析，请参阅以下文  
章：

Páll, S\. and Hess, B\. A flexible algorithm for calculating pair interactions on SIMD architectures\.  
Comput\. Phys\. Commun\. ____184____ , 2641–2650 \(2013\)\.↪http://dx\.doi\.org/10\.1016/j\.cpc\.2013\.06\.003

### 3\.8 使用 GROMACS 时的常见错误

##### GROMACS给出的绝大多数错误信息都是描述性的，告知用户确切的错误在哪里。下面列出了一些可能

##### 遇到错误，以及有关错误问题和解决方法的更多说明。

#### 3\.8\.1 使用过程中的常见错误

Out of memory when allocating 分配时内存不足

在计算中程序试图分配所需的内存，但由于内存不足而无法完成。

可能的解决方案：

减少用于分析的原子数目。

减少要处理的轨迹文件的长度。

在某些情况下，没有注意到GROMACS的长度单位为纳米而不是埃，用户生成的 pdb2gmx ↪ 297 水  
盒子是他们预期大小的 103 倍（例如，用于 gmx solvate ↪ 328 时）。

使用内存更大的计算机。

为计算机安装更多内存。  
用户应该记住，各种计算所需的时间和/或内存随原子/组/残基数 N 或模拟长度 T 的增长率为N，  
NlogN或N^2 （或者可能更糟\!），对 T 也是一样，具体取决于计算的类型。如果计算需要很长时间，考  
虑一下你在做什么，以及底层的算法（见参考手册↪ 469 ，手册页，或者使用程序的\-h选项），看看是否  
有更好的方法以减少计算时间。

#### 3\.8\.2 pdb2gmx 中的错误

Residue ’XXX’ not found in residue topology database 残基拓扑数据库中找不到残基 XXX

这意味着在运行 pdb2gmx ↪ 297 时，所选力场的残基数据库↪ 615 中没有残基XXX的相应条目。独立分子  
（如甲醛）或多肽（标准或非标准）都需要残基数据库↪ 615 中有相应的条目。这些条目定义了残基的原  
子类型，连接性，成键和非键相互作用类型，使用 pdb2gmx ↪ 297 构建 top ↪ 617 文件时必须借助于这些条目。  
缺失一个残基数据库↪ 615 条目可能是因为数据库中根本不包含这个残基，或者因为残基名称不同。  
对于新用户，出现此错误是因为他们正在使用自己的 PDB ↪ 614 文件运行 pdb2gmx ↪ 297 ，而没有考虑文件的  
内容。力场↪ 63 并不神奇，它只能处理残基数据库↪ 615 中已经提供，或者以其他方式包含的分子或残基  
（构建单元）。

如果想使用 pdb2gmx ↪ 297 自动生成所需的拓扑，你必须确保所需的力场↪ 63 中存在相应的 rtp ↪ 615 条目，并

且其名称与所用的构建单元相同。如果你的分子名称为HIS，那么 pdb2gmx ↪ 297 会尝试根据 rtp ↪ 615 文件

中的\[ HIS \]条目构建组氨酸，所以它会为组氨酸查找准确的原子条目，其他什么也不做。

如果你需要任意一个分子的 top ↪ 617 ，就不能使用 pdb2gmx ↪ 297 （除非你自己构建 rtp ↪ 615 条目）。你必须手

动构建需要的条目，或使用其他程序（例如 x2top ↪ 361 或用户提供的脚本）来构建 top ↪ 617 文件。

如果数据库中没有此残基的条目，获取力场参数的可能方法有：

看看残基数据库↪ 615 中对于此残基是否使用了不同的名称，如果是这样的，根据需要重命名残基，

自己对残基/分子进行参数化（需要很多工作，即使对专家也是如此）,

找到可用于分子的 top ↪ 617 ，将其转换为 itp ↪ 611 文件并包含在你的 top ↪ 617 文件中，

使用另一个力场↪ 63 ，其中包含所需的参数，

查阅原始文献，看看能否能找到与所用力场一致的残基参数。  
一旦你确定了自己残基的参数和拓扑，参考向力场中添加残基↪ 97 进行下一步的处理。

一旦确定了残基的参数和拓扑结构，请参考向力场中添加残基中的说明进行下一步处理\.

Long bonds and/or missing atoms 过长的键和 / 或缺失原子

所提供的 pdb ↪ 614 文件中可能缺失原子，导致 pdb2gmx ↪ 297 失败。检查 pdb2gmx ↪ 297 的屏幕输出，因为其中  
会给出缺失原子的具体信息。然后在 pdb ↪ 614 文件中添加缺失的原子，进行能量最小化保证其位置准确，  
或使用诸如 WHAT IF↪https://swift\.cmbi\.umcn\.nl/whatif/ 之类的程序固定侧链。

Chain identifier ’X’ was used in two non\-sequential blocks 两个非相邻单元使用了同样的链标识符 X

这意味着在用于 pdb2gmx ↪ 297 的坐标文件↪ 606 中，X链被拆分，这可能是由于错误地将一个分子插入到  
了另一个分子中。解决方法很简单：将插入的分子移动到文件中的某个位置，使得它不会再拆分另一个  
分子。此信息还可能意味着，两条单独的链使用了相同的链标识符。在这种情况下，将第二条链重命名  
为其他的唯一标识符。

WARNING: atom X is missing in residue XXX Y in the pdb file 警告： pdb 文件中的残基 XXX Y 缺  
失原子 X\.

与前面的过长键/缺失原子错误相关，通常这个错误的含义非常明显。也就是说，根据力场 rtp ↪ 615 文件  
中的条目， pdb2gmx ↪ 297 预期残基中存在某些原子。以下几种情况可能导致这个错误：

缺失氢原子；错误信息可能提示 hdb ↪ 611 文件中缺少相应的条目。更可能的是，所用文件中的氢原  
子名称与 rtp ↪ 615 条目中的不匹配。在这种情况下，可以使用\-ignh 选项让 pdb2gmx ↪ 297 自动添加  
正确的氢原子，或重命名有问题的氢原子。

末端残基（通常是N端）缺失H原子；这通常表明没有提供或选择正确的\-ter 选项。在使  
用 AMBER 力场↪ 43 时，问题通常是因为命名不一致。N端和C端残基的名称必须分别以N  
和C为前缀。例如，在 pdb ↪ 614 文件中N端丙氨酸的名称不应该是ALA，而应该是NALA，如  
ffamber↪http://ffamber\.cnsm\.csulb\.edu/ffamber\.php 说明中指定的那样。

提供给 pdb2gmx ↪ 297 的结构文件中只是简单地缺少原子；查看 pdb ↪ 614 文件中的REMARK 465 和  
REMARK 470条目。这些原子必须使用外部软件建模添加。GROMACS没有提供用于重建不完整  
模型的工具。

与错误信息所提示的相反，使用\-missing选项几乎总是不合适的。\-missing选项只应该利用 rtp ↪ 615  
条目，为类似氨基酸的分子生成专门的拓扑。如果你打算使用\-missing为蛋白质或核酸生成拓扑，请  
不要这么做；否则你得到的拓扑可能不符合物理实际。

____Atom X in residue YYY not found in rtp entry rtp____ 条目中不存在残基 ____YYY____ 的原子 ____X____

如果你使用 pdb2gmx ↪ 297 命令生成拓扑，那么原子名称应与 rtp ↪ 615 文件中的名称匹配，此文件定义了你  
的结构中的构建单元。在大多数情况下，问题是由名称不匹配引起的，因此只需适当地重新命名坐标文  
件↪ 606 中的原子即可。在其他情况下，提供的结构中有些残基可能不符合力场↪ 63 的要求，在这种情况  
下，你应该检查下为什么会这样，并根据自己发现的问题做出决定，例如，使用另一个力场↪ 63 ，或手动  
编辑结构等。

No force fields found \(files with name ’forcefield\.itp’ in subdirectories ending on ’\.ff’\) 找不到力场文  
件（在以 \.ff 结尾的子目录中名为 forcefield\.itp 的文件）

这意味着GROMACS的环境配置不正确，因为 pdb2gmx ↪ 297 无法找到其力场信息的数据库。这可能是因  
为将GROMACS安装从一个位置移动到了另一个位置。请按照使用 GROMACS ↪ 24 进行操作，或在操  
作之前重新安装GROMACS。

#### 3\.8\.3 grompp 中的错误

Found a second defaults directive file 发现第二个包含默认指令的文件

这是由于 \[ defaults \]指令多次出现在系统的拓扑↪ 617 或力场↪ 63 文件中引起的，因为它只能出现  
一次。出现这种错误的一个典型原因是，在其他来源的包含拓扑↪ 617 文件 itp ↪ 611 中设置了第二个 \[  
defaults \]指令。有关拓扑文件的格式规范，见参考手册↪ 469 5\.6节：

\[ defaults \]  
; nbfunc comb\-rule gen\-pairs fudgeLJ fudgeQQ  
1 1 no 1\.0 1\.0

一种简单的解决方法是，注释掉（或删除）文件中第二次包含\[ defaults \]指令的代码行，即：

;\[ defaults \]  
; nbfunc comb\-rule gen\-pairs fudgeLJ fudgeQQ  
; 1 1 no 1\.0 1\.0

更好的解决方法是重新思考一下你的做法。\[ defaults \]指令只应该出现在 top ↪ 617 文件的顶部，你指  
定力场↪ 63 的地方。如果你试图混合两个力场↪ 63 ，那么你就是在自找麻烦。如果一个分子 itp ↪ 611 文件试  
图选择一个力场，那么生成文件的人就是在自找麻烦。

Invalid order for directive xxx 指令 xxx 的顺序错误

\.top和\.itp文件中的指令要遵循一定的出现顺序规则，如果违反了这些规则就会出现此错误。考虑下参  
考手册第 5 章↪ 524 和/或教程中的示例和讨论。包含文件机制↪ 34 不能用于在任何旧的位置\#include文  
件，因为它们包含指令，而这些指令必须正确放置。

特别是，出现Invalid order for directive defaults 错误是因为在拓扑↪ 617 或力场↪ 63 文件中\[  
defaults \]的位置不正确；\[ defaults \]指令只能出现一次，而且必须是拓扑↪ 617 中的第一个指令。  
\[ defaults \]指令通常出现在力场↪ 63 文件（forcefield\.itp）中，当你\#include此文件到系统拓  
扑时，\[ defaults \]指令就会添加到拓扑↪ 617 中。

如果出现问题的指令是 \[ atomtypes \] （这是此错误的最常见来源）或其他任何成键或非键的 \[  
\*types \]指令，通常的原因是用户增加了一些非标准物种（配体，溶剂等）并引入了新的原子类型或  
参数。如上所述，这些新类型和参数必须出现在任何\[ moleculetype \]指令之前。力场↪ 63 必须在定  
义任何分子之前完全构建完成。

Atom index n in position\_restraints out of bounds 位置限制中的原子索引 n 超出了范围

一个常见问题是放置多个分子的位置限制文件时没有按照顺序。记住，位置限制 itp ↪ 611 文件中的\[  
position\_restraints \]只能属于包含它的\[ moleculetype \]。

System has non\-zero total charge 系统的总电荷非零

通知你可能需要添加抗衡离子来中和系统的净电荷，或者拓扑结构可能存在问题。

如果电荷并不是非常接近整数，则表明拓扑↪ 617 存在问题。如果使用的是 pdb2gmx ↪ 297 ，那么请查看下原  
子列表右侧的注释列，其中列出了累计的总电荷。在每个残基（和/或电荷组，如果适用的话）之后，累  
计值应该是整数。这有助于发现从那个残基开始总电荷偏离整数值。还要检查使用的封端原子组。

如果总电荷已经接近整数值，那么差异是由舍入误差↪ 69 引起的，并不是太大的问题。

PME用户注意：在PME中可以使用均匀的中和背景电荷来对具有净背景电荷的系统进行补偿。然而，

这可能会导致不需要的假象，特别是对于非均相系统，见论文 \(^181\) ↪ 714 （http://pubs\.acs\.org/doi/abs/10\.  
1021/ct400626b）。无论如何，添加抗衡离子使得系统整体呈电中性是标准做法。  
Incorrect number of parameters 参数个数不正确  
检查系统的拓扑↪ 617 文件。对其中的一个成键项，你没有提供足够数目的参数。有时，如果你在编辑文  
件时破坏了包含文件机制↪ 34 或拓扑文件格式（见参考手册第 5 章↪ 524 ），也会发生这种情况。  
Number of coordinates in coordinate file does not match topology 坐标文件中的粒子数与拓扑文件  
不匹配  
这个错误指出，根据 top ↪ 617 文件 top ↪ 617 提供的信息，系统中原子或粒子的总数，与坐标文件↪ 606 ，通常  
是 gro ↪ 610 或 pdb ↪ 614 文件，提供的总数不匹配。  
最常见的原因很简单，用户在对系统进行溶剂化，或向其中添加其他分子后没有更新拓扑文件，或者更  
新时系统中的分子数目出现了输入错误。确保正在使用的拓扑文件的末尾包含类似于下面的内容，它们  
与所使用的坐标文件中的内容完全匹配，包括分子的数目和出现顺序：  
\[ molecules \]  
; Compound \#mol  
Protein 1  
SOL 10189  
NA\+ 10  
Fatal error: No such moleculetype XXX 致命错误：没有分子类型 XXX  
top ↪ 617 文件末尾的 \[ molecules \] 中的每类分子都必须有相应的 \[ moleculetype \]，它们必须  
在 top ↪ 617 文件或者包含↪ 34 itp ↪ 611 文件中预先定义。有关语法说明，见参考手册↪ 469 5\.6\.1节。你的 top ↪ 617  
文件没有对指定的分子进行定义。检查相关文件的内容，分子如何命名的，后面如何引用它们的。注意  
\#ifdef和/或\#include语句的状态。

T\-Coupling group XXX has fewer than 10% of the atoms 温度耦合组 XXX 的原子数不到 10%

可以为模拟中的每个分子类型指定单独的控温器↪ 58 （温度耦合组）。在进行分子动力学模拟时，许多  
新用户会采用这种特别糟糕的做法。这样做不是个好主意，因为你可能会引入很难预测的错误和假象。  
在某些情况下，最好是使用默认的 System组将所有分子放在一个温度耦合组中。如果需要使用单独  
的耦合组来避免 热溶剂，冷溶质问题，那么确保每个组的粒子数目 足够多，并且将在模拟中会一  
起出现的分子类型放到同一个组中。例如，对于含有抗衡离子的水中的蛋白质，可以使用Protein和  
Non\-Protein两个组。

The cut\-off length is longer than half the shortest box vector or longer than the smallest box diagonal  
element\. Increase the box size or decrease rlist 截断长度大于最短盒子向量长度的一半或大于最小盒  
子对角线的长度。增加盒子大小或减少 rlist

错误信息指出了问题所在。盒子尺寸太小会使得原子与其自身相互作用（当使用周期性边界条件时），因  
此违反了最小映像约定。这是完全不符合实际的，并会引入严重的假象。解决方案也就是信息中给出的  
注意事项，或者增加模拟盒子的大小，使其在所有三个维度上的长度都至少是截断长度的两倍（还要注  
意，如果使用压力耦合，盒子大小会随时间变化，如果只是略微减小，仍然会违反最小映像约定），或者  
减少截断长度（取决于所用的力场↪ 63 ，可能无法使用这种解决方法）。

Atom index \(1\) in bonds out of bounds 键中的原子索引 \(1\) 超出范围

这类错误如下所示：

Fatal error:  
\[ file spc\.itp, line 32 \]  
Atom index \( 1 \) in bonds out of bounds \( 1 \- 0 \)\.  
This probably means that you have inserted topology  
section"settles" in a part belonging to a different  
molecule than you intended to\. in that case move the  
"settles"section to the right molecule\.

错误原因不言自明。你应该查看自己的 top ↪ 617 文件并检查所有\[ molecules \]部分是否包含了与该分  
子有关的所有数据，而没包含其他数据。也就是说，在前一个 \[ moleculetype \]结束之前，你不能  
\#include另一个分子类型（ itp ↪ 611 文件）。关于不同\[ sections \]的顺序，见参考手册第 5 章↪ 524 中  
的示例。注意使用\#include包含↪ 34 的任何文件的内容

如果所选力场↪ 63 默认情况下不支持你所用的水模型，也会出现这个错误。例如，如果你试图将SPC水  
模型与 AMBER 力场↪ 43 一起使用，就会看到此错误。原因在于，在spc\.itp中，没有使用\#ifdef语  
句为任何 AMBER 力场↪ 43 的原子类型进行定义。你可以自己添加需要的定义，也可以使用其他水模型。

____XXX non\-matching atom names XXX____ 不匹配的原子名称

这个错误通常表示拓扑↪ 617 文件的顺序与坐标文件↪ 606 的顺序不匹配。运行 grompp ↪ 252 时，程序会读  
取拓扑↪ 617 ，将其中的参数映射到坐标↪ 606 文件中的原子上。如果不匹配，就会导致此错误。要解决这个  
问题，请确保\[ molecules \]指令的内容与坐标文件中原子的顺序完全匹配。

在少数情况下，此错误没有关系。也许你使用的坐标↪ 606 文件中离子的名称来自旧版本（4\.5之前）的  
GROMACS。在这种情况下，可以让 grompp ↪ 252 重新分配名称。对于任何其他情况，出现此错误时，不  
应忽略。仅仅因为可以使用\-maxwarn选项并不意味着你应该在模拟工作中盲目地希望使用它。毫无疑  
问，模拟会爆破↪ 60 。

The sum of the two largest charge group radii \(X\) is larger than rlist \- rvdw/rcoulomb 两个最大电  
荷组半径 \(X\) 的总和大于 rlist \- rvdw/rcoulomb

此错误警告，某些设置组合会导致最长截断处的能量守恒性较差，这种情况发生在电荷组移入或移出配  
对列表范围时。此错误可能有两个来源：

- 你的电荷组包含了太多原子。大多数电荷组应小于 4 个原子或更少。
- 你的 mdp ↪ 612 设置与所选算法不兼容。对于切换或移位函数，rlist 必须大于最长截断值（rvdw  
或rcoulomb），以便为移出邻区搜索半径的电荷组提供缓冲空间。如果设置不正确，可能会漏掉  
一些相互作用，导致能量守恒不佳。

在以下两种情况下会出现类似的错误\(The sum of the two largest charge group radii \(X\) is larger than  
rlist\):

- 电荷组太大或rlist设置得太小。
- 分子在周期性边界处被打断，对周期性系统这不是问题。在这种情况下，两个最大电荷组的总和会  
对应于沿分子被打断的盒子向量方向的两倍。

Invalid line in coordinate file for atom X 坐标文件中原子 X 的行无效

如果以某种方式破坏了 gro ↪ 610 文件的格式，就会出现此错误。最常见的原因是， gro ↪ 610 文件中的第二行  
指定了不正确的原子数，导致 grompp ↪ 252 继续读取原子却读到了盒子向量。

#### 3\.8\.4 mdrun 中的错误

Stepsize too small ， or no change in energy 。步长太小，或能量没有变化。收敛到机器精度，但未收敛  
到指定的 Fmax

这可能不是错误。它只是简单地告诉你，在能量最小化过程中，使用当前的参数，mdrun最小化的结构  
已经达到了可能的极限。这并不意味着系统最小化不完全，但在某些情况下确实可能意味着最小化不完  
全。如果系统中存在大量的水，那么Epot的数量级为\-10^5 到\-10^6 （同时Fmax在 10 到1000 kJ mol\-1  
nm\-1之间）通常是合理，可以使用得到的结构启动大多数MD模拟。最重要的结果可能是Fmax的值，  
因为它描述了势能面的斜率，即结构离能量最小点的距离有多远。只有出于特殊的目的，例如要进行简  
正模式分析之类的计算，才可能需要进一步最小化。进一步的能量最小化可以通过使用不同的能量最小  
化方法或使用双精度的GROMACS来实现。

Energy minimization has stopped because the force on at least one atom is not finite 能量最小化已  
经停止，因为至少有一个原子上的力无穷大。

这可能表示在输入坐标中（至少）有两个原子距离太近，并且二者之间的相互作用力的大小超过了  
GROMACS精度可以表示的范围，因此无法进行最小化。有时可以通过使用软核势来最小化具有无限力  
的系统，它可以使用GROMACS自由能代码来缩小Lennard\-Jones相互作用的大小。这种方法是一种  
可以接受的工作流程，可用于平衡一些粗粒化系统，如Martini。

LINCS/SETTLE/SHAKE 警告

有时，在运行动力学过程中， mdrun ↪ 276 可能会将一系列与约束算法（如LINCS，SETTLE或SHAKE）  
有关的警告输出到 log ↪ 611 文件，然后突然终止执行（可能还会输出一些 pdb ↪ 614 文件）。这些约束算法通  
常用于约束键长和/或键角。当一个系统爆破↪ 60 （即由于力过大而爆炸）时，约束通常会首先失败。这  
并不一定意味着你需要排查约束算法的问题。通常情况下，这表明你的系统存在一些更根本（不符合物  
理实际）的错误。另请参阅如何判断不稳定的系统↪ 61 中的建议。

1\-4 interaction not within cut\-off 1\-4 相互作用不处于截断范围内

一些原子在移动后，其中被三条键分开的两个原子之间的距离超过了截断距离。这不是好兆头。最重要  
的是，不要增大截断距离\!这个错误实际上表明，有些原子的速度非常大，这通常意味着分子（的一部  
分）发生了爆破↪ 60 。如果使用LINCS约束算法，那么可能还会出现很多LINCS警告。当使用SHAKE  
约束算法时，这会导致SHAKE错误，因此在出现1\-4 not within cutoff错误之前模拟就会停止。

系统中的粒子速度非常大的可能原因有很多。如果在模拟开始时就发生了这种情况，那么你的系统可能  
没有平衡好（例如，系统中有些原子间的距离过近）。试试再进行一次能量最小化能不能解决问题。否  
则，可能系统的温度过高，和/或时间步长过大。试着调整下这些参数，直到不再出现错误。如果仍然不  
能解决问题，请检查拓扑↪ 617 文件中参数是否合理\!

模拟在运行但没有输出

这并不是错误，只是mdrun似乎占用了CPU时间，但还没有向输出文件中写入任何东西。出现这种情  
况的原因有很多：

- 模拟可能（非常）慢↪ 74 ，并且由于存在输出缓冲，因此可能需要相当长的时间才能在相应的文件中  
显示输出。如果你需要修复某些问题并希望尽快获得输出，那么可以将环境变量GMX\_LOG\_BUFFER  
设置为 0 。
- 模拟可能出现了问题，例如产生了非数值（NAN）错误（可能的原因包括除以零）。使用NAN进  
行后续计算会导致浮点异常，从而引起所有操作的速度都会成数量级地降低。
- 你可能将所有nst\*参数（在你的 mdp ↪ 612 文件中）都设置为 0 ，这样会忽略大多数输出。
- 你的磁盘可能已经没有空间了。这最终会导致 mdrun ↪ 276 崩溃，但由于存在输出缓冲，mdrun可能  
需要一段时间才能发现它无法写入文件。

##### 3\.8\. 使用 GROMACS 时的常见错误 

Can not do Conjugate Gradients with constraints 带约束的系统无法使用共轭梯度方法

这意味着，如果拓扑中定义了约束，就无法使用共轭梯度算法进行能量最小化。请查看参考手册↪ 469 。

Pressure scaling more than 1% 压力缩放超过 1%

当模拟盒子开始振荡时（由于大的压力和/或小的耦合常数），往往会出现这个错误。如果不进行干预，  
系统会开始共振并且最终崩溃↪ 60 。这可能意味着，在使用压力耦合之前系统并未充分平衡。因此，进行  
更多/更好的平衡可以解决这个问题。

建议查看下碰撞发生前和碰撞发生过程中的系统轨迹。这可能告诉你系统/结构的某些特殊部分是否存  
在问题。

在某些情况下，如果系统已经充分平衡，这个错误可能意味着压力耦合常数 tau\-p ↪ 138 太小（特别是使  
用Berendsen弱耦合方法时）。增大耦合常数的值可以减缓对压力变化的响应，并可能防止共振发生。如  
果对尚未平衡好的系统使用Parrinello\-Rahman压力耦合，你更有可能看到这个错误。建议首先使用更  
稳健的Berendsen方法，然后再换用其他算法。

在不存在约束和/或虚拟位点的情况下，如果使用的时间步长过大，如5 fs，也会出现这个错误。

Range Checking error 范围检查错误

这通常意味着你的模拟发生了爆破↪ 60 。可能你需要进行更好的能量最小化和/或平衡，和/或使用更好的  
拓扑。

X particles communicated to PME node Y are more than a cell length out of the domain decom\-  
position cell of their charge group 通信到 PME 节点 Y 的 X 个粒子超过了其电荷组的区域分解单元  
格的长度

这是 mdrun ↪ 276 告知系统发生爆破↪ 60 的另一种方式。如果粒子穿过了整个系统，就会导致这个致命错  
误。此信息表明系统的某些部分正在发生破碎（因此超出了“其电荷组的单元格”）。关于如何解决此问  
题的建议，请参阅爆破↪ 60 页面。

A charge group moved too far between two domain decomposition steps 。在两个区域分解步骤之间  
电荷组移动得太远。

见上面的信息。

Software inconsistency error: Some interactions seem to be assigned multiple times 软件不一致错  
误：某些相互作用似乎被分配了多次

见上面的信息

There is no domain decomposition for n ranks that is compatible with the given box and a minimum  
cell size of x nm 对于 n 个进程，无法进行符合给定盒子大小，且最小单元格尺寸为 x nm 的区域分解

这意味着你试图运行并行计算，当 mdrun ↪ 276 尝试划分模拟单元格时，无法进行。最小单元格尺寸由最  
大电荷组或成键相互作用的大小，以及rvdw，rlist和rcoulomb的最大值，键约束的其他一些影响，  
安全边界等控制。因此，不可能使用大量处理器运行小型模拟。所以，如果 grompp ↪ 252 警告你电荷组很  
大，你需要注意并重新考虑下它的大小。 mdrun ↪ 276 会在 log ↪ 611 文件中输出计算最小单元格尺寸的详细  
信息，因此你或许可以在那里找到错误的原因。

如果你认为自己并没有运行并行计算，请注意，自4\.5版本起GROMACS默认使用基于线程的并行。  
要禁用默认的并行，可以为 mdrun ↪ 276 指定\-ntmpi 1命令行选项。否则，你可能正在使用启用MPI的  
GROMACS却没有意识到这一事实。

### 3\.9 术语

#### 3\.9\.1 压强

##### 分子动力学中的压力可以由动能和维里来计算。

##### 波动

##### 无论模拟中是否使用压力耦合，模拟盒子的压力值都会显著振荡。瞬时压力没有意义，而且没有明确定

##### 义。在皮秒时间尺度上，它通常也不能很好地表征真实压力。这种变化是完全正常的，因为压力是一种

##### 宏观性质，只能适当地测量其时间平均值，而在微观尺度上则通过压力耦合对其进行测量和/或调节。它

##### 的变化程度和速度取决于系统中的原子数，所用压力耦合的类型和耦合常数的值。典型的波动可以是数

##### 百巴。对于含 216 个水分子的盒子，标准的波动是500\-600巴。由于波动随粒子数目的平方根而下降，

##### 因此含 21600 个水分子（ 100 倍大）的系统仍会具有50\-60巴的压力波动。

#### 3\.9\.2 周期性边界条件

##### 分子动力学模拟使用周期性边界条件（PBC）来避免因模拟尺寸有限而引起的边界效应问题，使得系统

##### 更像一个无限大的系统，而代价是可能的周期性效应。

##### 可视化轨迹的初学者有时会认为他们发现了问题，当

##### • 分子没有停留在盒子的中心，或者

##### • 看起来（部分）分子从盒子中扩散出来，或者

##### • 出现了孔洞，或者

##### • 出现了破碎的分子，或者

##### • 他们的晶胞是菱形十二面体或立方八面体，但模拟后它看起来像一个倾斜的立方体，或者

##### • 出现了穿过整个模拟单元的不合理成键。

##### 这并不是问题或错误，而是你应该预期看到的。

##### PBC的存在意味着，任何离开模拟盒子的原子，比如从右侧面离开，然后会从左侧面进入模拟盒子。在

##### 大蛋白质的例子中，如果你看一下模拟盒子与蛋白质突出的表面相对的面，就会发现溶剂中的孔洞。分

##### 子从盒子内的最初位置移动出去的原因（对于绝大多数模拟）是它们可以自由扩散。因此它们就这样做

##### 了。它们并不会被固定在盒子中的神奇位置。执行模拟时，盒子不以任何东西为中心。当然，分子并不

##### 是完整的。此外，任何周期性的晶胞形状都可以表示为平行六面体（也就是三斜晶胞），GROMACS会

##### 在内部进行转换，而不考虑盒子的初始形状。

这些可视化问题可以在模拟结束后进行修复，只要选择合适的选项使用 gmx trjconv ↪ 343 来处理轨迹文件

即可。类似地，在分析诸如原子位置的RMSD之类的量时，如果直接将需要调整周期性的结构与参考

结构进行比较，所得结果可能不对，使用 gmx trjconv ↪ 343 的解决方法与前面所说的相同。在一些复杂的

情况下，需要进行多次操作，因此需要多次调用 gmx trjconv ↪ 343 。

详细信息请参阅参考手册↪ 478 中的相应章节。

##### 建议的工作流程

使用 gmx trjconv ↪ 343 修复周期性效果，以便进行可视化或分析可能很棘手。有时可能需要多次调用。你

可能需要创建自定义索引组（例如将配体与蛋白质保持在一起）。按照下面的步骤（省略了那些不需要

的）应该会得到正确的结果。你需要查阅gmx trjconv \-h以了解每一步的详细信息。这么做是故意的

- 没有神奇的咒语能让你一步完成。首先，你必须决定你想要什么。:\-\)  
1\.首先，如果你需要完整的分子，那就让它们变得完整。  
2\.如果你希望分子/粒子聚集在一起，那就把它们聚集在一起。  
3\.如果你需要移除跳动，那么抽取轨迹中的第一帧作为参考，然后使用\-pbc nojump处理轨迹。  
4\.使用某些标准将系统居中。这样做系统会发生偏移，因此在此步骤之后不能再使用\-pbc nojump。  
5\.也许可以使用其他\-pbc或\-ur选项将所有粒子都置于盒子中。  
6\.将得到的轨迹叠合到某个（其他）参考结构（如果需要的话），之后不要再使用任何与PBC相关  
的选项。  
对于第三点，问题是 gmx trjconv ↪ 343 使用 \-s 指定的参考结构从第一帧中移除了跳动。如果参考结构  
（运行输入文件）不是团簇/完整的，使用\-pbc nojump会撤消步骤 1 和 2 的操作。

#### 3\.9\.3 控温器

##### 控温器用于帮助模拟从正确的系综（即NVT或NPT）中进行采样，具体作法是通过某种方式调节系统

##### 的温度。首先，我们需要确定温度的含义。在模拟中，“瞬时（动能）温度”通常利用能量均分定理根据

##### 系统的动能计算。换句话说，温度是根据系统的总动能计算出来的。

##### 那么，控温器的目标是什么?实际上，它的目标不是保持温度不变，因为那意味着总动能不变，这是愚

##### 蠢的做法，而且不是NVT或NPT的目标。相反，它是为了确保系统的平均温度是正确的。

##### 要知道为什么会这样，想象一下房间里的一杯水。假定你可以非常仔细地观察玻璃杯某些小区域中的几

##### 个分子，并测量它们的动能。你不会期望对这么少的粒子来说，其动能会精确地保持不变；相反，你会

##### 期望，由于粒子数目很少，动能会波动。当你对越来越多的粒子进行平均时，平均值的波动会变得越来

##### 越小，因此最后当你看到整个玻璃杯时，你会说它具有“恒定的温度”。

##### 与一杯水相比，分子动力学模拟的系统通常非常小，因此波动会更大。因此，在这种情况下，更合适的

##### 方式是将控温器的作用视为确保

\(a\)系统具有正确的平均温度，以及

\(b\)波动的大小正确。

58 第 3 章 用户指南

##### 有关如何应用温度耦合以及当前可使用哪些温度耦合类型的详细信息，见参考手册↪ 495 中的相关章节。

##### 该怎么做

##### 关于实际应用的一些的提示，它们通常都是好主意：

##### • 除了提供正确的平均温度外，使用的控温器最好能对温度的正确分布进行采样（例如，请参阅手册

##### 相应章节）。

##### • 至少：使用一个能给出正确的平均温度的控温器，并把它应用到系统中那些合适的组分上（参见不

要做什么↪ 59 中的第一个要点）。在某些情况下，使用 tc\-grps = System可能会导致”热溶剂/冷

溶质”问题，具体说明见进一步阅读材料↪ 59 中的第 3 篇参考文献。

##### 不要做什么

##### 关于实际应用的一些的提示，它们通常不是好主意：

##### • 不要为系统的每个组分使用单独的控温器。一些分子动力学控温器只在热力学极限下才有效。一

##### 个组必须足够大，使用单独的控温器才是合理的。如果你将一个控温器用于小分子，另一个用于蛋

##### 白质，另一个用于水，很可能会引入难以预测的误差和假象。尤其是，不要将溶剂中的离子与溶剂

分开进行单独耦合。对于蛋白质模拟，使用tc\-grps = Protein Non\-Protein通常是最好的。

- 对于自由度较少的系统，不要使用那些只在自由度很大的极限情况下才有效的控温器。例如，不要  
将Nosé\-Hoover或Berendsen控温器用于自由能计算的分子类型，因为在这种情况下，系统中的  
某个组分在终止状态下具有很少的自由度（即一种无相互作用的小分子）。

#### 3\.9\.4 能量守恒

##### 原则上，分子动力学模拟应该保持总能量，总动量以及（在非周期系统中）总角动量守恒。许多算法和

##### 数值问题使得情况并非总是如此：

- 截断处理和/或长程静电处理（参见Van Der Spoel, D\. & van Maaren, P\. J\. The origin of layer

structure artifacts in simulations of liquid water\. J\. Chem\. Theor\. Comp\. ____2____ , 1–11 \( \(^2006\) ↪https:  
//doi\.org/10\.1021/ct0502256\)\.）

- 对列表的处理，
- 约束算法（参见，例如Hess, B\. P\-LINCS: A parallel linear constraint solver for molecular simula\-

tion\. J\. Chem\. Theor\. Comp\. ____4____ , 116–122 \( \(^2008\) ↪https://doi\.org/10\.1021/ct700200b\)\.）。

- 积分时间步长。

##### • 温度耦合↪ 58 和压力耦合↪ 57 。

- 舍入误差（尤其是单精度），例如减去大数（Lippert, R\. A\. et al\. A common, avoidable source of

error in molecular dynamics integrators\. J\. Chem\. Phys\. ____126____ , 046101（ \(^2007\) ↪http://dx\.doi\.org/10\.1063/  
1\.2431176）\.）。

- 积分算法的选择（在GROMACS中通常使用跳蛙式）。
- 移除质心运动：对多个组这样处理时，会违反能量守恒。

#### 3\.9\.5 平均结构

##### 各种GROMACS实用程序可以计算平均结构。据推测，这一想法来自类似于系综平均核磁共振结构这

##### 样的概念。在某些情况下，计算平均结构是有意义的（例如，在计算均方根涨落（RMSF\)的过程中，需

##### 要所有原子的平均位置）。

##### 然而，重要的是要记住，平均结构不一定有意义。类比一下，假设我左手拿着一个球，然后换到右手，如

##### 此交替进行。球的平均位置在哪里?介于两者之间\-即使我总是用左手或右手拿着它。类似地，对于结

##### 构，只要存在单独的亚稳构象状态，其平均值就会变得毫无意义。这可能发生在侧链，或骨架的某些区

##### 域，甚至整个螺旋或二级结构的组分。

##### 因此，如果你从分子动力学模拟得到了一个平均结构，并发现不合理的键长，奇怪的结构等假象，这并

##### 不一定意味着错误。它只是表明了上述情况：由模拟得出的平均结构不一定是有物理意义的结构。

#### 3\.9\.6 爆破

爆破（Blowing Up）是一个相当专业的术语，用于描述常见的模拟失败。简而言之，它描述了一种常见  
的模拟失败类型，通常是由于出现了极大的相互作用力而最终导致积分步骤失败引起的。

稍微展开一下背景，我们必须清楚，分子动力学的基本原理是在非常短的，离散的时间步长内对牛顿运  
动方程进行数值积分，借助这些时间步，根据粒子在前一时间步的速度，位置，受力来确定下一时间步  
的新的速度和位置。如果在某一时间步中作用力变得太大，就会导致在到达下一时间步时粒子的速度/位  
置发生极大的变化。通常，这会导致一连串的错误：一个原子在某一时间步受到了很大的作用力，因此  
在下一时间步中它可能失控并击穿整个系统，最终超出它应在的位置，或与其他原子发生重叠，或发生  
其他类似的情形。这又导致下一时间步中产生了更大的作用力，更不受控的运动。依此类推。这种情况  
延续下去，最终，会导致模拟程序以某种方式崩溃，因为它无法处理这种情况。在有约束的模拟中，这  
种情况的最初征兆通常是出现一些LINCS或SHAKE警告或错误，这并非这些约束导致的，而是因为  
受到影响后它们最先崩溃。类似的，在使用区域分解的模拟中，你可能会看到类似粒子移动的距离超出  
其电荷组区域分解单元长度的信息，这也是系统潜在问题的征兆，而不是区域分解算法自身的问题。此  
外，有关表格或1\-4相互作用处于表格支持距离范围外的一些警告也是如此。由于这些模拟在不同的计  
算机系统上不具有数值重现性，在一台计算机上模拟出现爆破，而在另外的计算机上模拟可能会稳定。

导致爆破的可能原因包括：

- 能量最小化不彻底；
- 初始构型不合理，可能存在空间冲突；
- 使用的时间步长过大（尤其是带有约束的情况下）;
- 在自由能计算中进行粒子插入时没有使用软核势；
- 使用了不合适的压力耦合算法（例如，在没有达到平衡时，Berendsen方法能够很好地弛豫体积，
- 但接下来需要换到更精确的压力耦合算法）;

##### • 使用了不合适的温度耦合，或许用在了不合适的组上；或者

##### • 对粒子坐标进行的位置限制与当下系统中的坐标差别太大；或者

##### • 系统内某处有一个水分子与其他水分子独立开来；或者

- 遇到了 gmx mdrun ↪ 276 中的bug。

由于爆破通常是由于特定时间步长下作用力过大导致的，因此基本的解决方法有以下两种：

- 确保作用力不会过大；或者
- 使用更小的时间步长。

如果问题出现在模拟的开始阶段，更好的系统准备工作有助于确保力不会过大。

#### 3\.9\.7 如何诊断一个不稳定的系统

##### 对一个爆破的系统进行错误排查可能是一项具有挑战性的工作，尤其是对于那些没有经验的用户来说。

##### 当处理这种情况时，以下几点建议通常会有所帮助：

1\.如果崩溃发生得相当早（几个模拟步之内），将nstxout（或nstxout\-compressed）设置为 1 ，

收集所有可能的帧。观察得到的轨迹，看看是哪些原子/残基/分子首先变得不稳定；

2\.试着简化问题来确定原因：

- 如果你模拟的是一个溶剂构成的盒子，试着先对单个溶剂分子进行能量最小化以及模拟，看  
看系统的不稳定性是由分子拓扑的内在问题引起的，还是由初始构型中分子位置存在冲突引  
起的；
- 如果你模拟的是蛋白质\-配体系统，试着将蛋白质单独放置在所需溶剂中进行模拟。如果蛋白  
质是稳定的，将配体分子单独放在真空中进行模拟，看看其拓扑是否能提供稳定的构型，能  
量等；
- 删除所用的花哨算法（LINCS/SHAKE），尤其在没有达到充分平衡的时候  
3\.使用 gmx energy ↪ 237 监测系统各个能量组分的变化。例如，如果分子内的能量项出现了尖峰，可能  
意味着使用了不正确的成键参数。  
4\.确保没有忽略错误信息（运行 gmx pdb2gmx ↪ 297 时缺失原子，运行 gmx grompp ↪ 252 时原子名称不  
匹配，等等），或者使用了变通方法来保证你的拓扑文件完整并能被正确解释（例如使用了 gmx  
grompp \-maxwarn来忽略不能忽略的警告）;  
5\.确保在 mdp ↪ 612 文件中为你的系统和所选力场设置了合适的选项，尤其是截断的处理，合适的邻区  
搜索间隔（nstlist）以及温度耦合。就算系统的初始构型是合理的，设置不当也会导致物理模型  
崩溃。

如果使用隐式溶剂，在预平衡阶段使用比成品MD阶段更小的时间步长可以使能量平衡更稳定。

在几种常见的情形下经常出现不稳定性，通常是向系统中引入新物种（配体或其他分子）的时候。要确  
定问题的根源，就得将系统（如蛋白质\-配体复合物系统）简化一下，拆开来逐步分析：

1\.蛋白质自身（在水中）能否充分进行能量最小化?这是对蛋白质分子坐标完整性和系统准备工作的

一个测试。如果失败了，说明在运行 gmx pdb2gmx ↪ 297 时可能出错了（说明见下文），或者使用 gmx

genion ↪ 249 添加离子时，有些离子的位置离蛋白质太近了（毕竟是随机加入的）。

##### 3\.9\. 术语 61

##### 2\.配体分子在真空中能否进行能量最小化?这是对其拓扑的测试。如果不能，检查配体分子的参数化

##### 过程以及任何加入力场文件中的新参数。

##### 3\.（如果之前几项都成功了）配体分子在水中进行能量最小化，或直接运行一段短时间的模拟，是否

##### 成功?

##### 还有一些问题可能来自于生物分子的拓扑自身：

1\.在运行 gmx pdb2gmx ↪ 297 时是否使用了\-missing选项?如果是，请不要使用该选项。重新构建缺

失的坐标而不是忽略它们。

2\.是否通过改变键长而忽略了存在太长/太短键的警告?如果是，请不要使用该选项。这说明可以存

在原子缺失或形成了一些糟糕的输入结构。^1

#### 3\.9\.8 分子动力学

##### 分子动力学（MD）是基于一些基本的物理定律与原子和/或分子的相互作用进行的计算机模拟。

##### GROMACS参考手册↪ 482 对此领域提供了很好的一般性介绍，以及与GROMACS使用有关的特定材

##### 料。对于任何希望使用GROMACS的人来说，前几章都是必读的，并不是浪费时间。

- 分子建模的简介（幻灯片↪https://extras\.csc\.fi/chem/courses/gmx2007/Erik\_Talks/preworkshop\_tutorial\_introduction\.pdf，  
视频↪https://video\.csc\.fi/playlist/dedicated/0\_7z3nas0q/0\_tccn9xof）\-理论框架，建模层面，局限性和可能性，系  
统和方法（Erik Lindahl）。

##### 书籍

##### 有一些教科书。

##### 好的导论性教科书：

- A\. Leach \(2001\) Molecular Modeling: Principles and Applications
- T\. Schlick \(2002\) Molecular Modeling and Simulation

需要编程基础的：

- D\. Rapaport \(1996\) The Art of Molecular Dynamics Simulation
- D\. Frenkel, B\. Smith \(2001\) Understanding Molecular Simulation

物理视角更多的书籍：

- M\. Allen, D\. Tildesley \(1989\) Computer simulation of liquids
- H\.J\.C\. Berendsen \(2007\) Simulating the Physical World: Hierarchical Modeling from Quantum  
Mechanics to Fluid Dynamics

\(^1\) 总得来说，LINCS/SHAKE warning的出现还是因为体系没有平衡好。往往我们在进行了能量最小化后还是偶尔会遇到这  
个问题，而且一般出现在NPT平衡阶段（NVT因为没有加压所以出现警告的概率较小）。在确认拓扑没有问题的前提下，可以  
先进行一段时间步长较小的平衡来弛豫体系，往后再进行较大时间步长的平衡。当然，也可以使用不同的压力耦合算法来实现快  
速弛豫体系的效果。【刘恒江】

##### 类型 / 系综

##### • NVE \-粒子数（N），系统体积（V）和能量（E）恒定/守恒。

##### • NVT \-粒子数（N），系统体积（V）和温度（T）恒定/守恒。\(关于恒定温度的更多信息参见恒温

##### 器↪ 58 \)。

##### • NPT \-粒子数（N），系统压力（P）和温度（T）恒定/守恒。\(关于恒定压力的更多信息参见压力

##### 耦合↪ 57 \)。

#### 3\.9\.9 力场

##### 力场是势函数和参数化相互作用的集合，可用于研究物理系统。对其历史，功能和使用的一般性介绍超

出了本指南的范围，用户可以查阅相关文献或试着从相关的 维基百科页面↪https://en\.wikipedia\.org/wiki/Force\_  
field\_\(chemistry\) 开始了解。

下面仅给出一些简单说明。

力场用以描述粒子（通常是原子）之间的相互作用，包含两个主要部分：

- 用于描述势能及其导数（力）的一组方程（称为势函数）。
- 这组方程中使用的参数

在一组方程中，可以使用各种不同的参数集。必须注意，方程与参数的组合应当自洽。一般来说，对参  
数集的一部分进行临时更改是危险的，因为对合力的各种贡献通常是相互依赖的。特别是，没有理由假  
定，用一种力场处理体系的一部分，而用另一种力场处理体系的另一部分，会得到任何有意义的结果。  
同样，也没有理由假定力场的“键强度”参数与任何实际测量的键强度有任何特定的相关性。

有三种类型的力场：

- 全原子力场：需要为体系中的每个单个原子提供参数。
- 联合原子力场：需要为除非极性氢之外的所有原子提供参数。
- 粗粒化力场：通过将几个原子视为“超级原子”来抽象地表示分子。

#### 3\.9\.10 约束与限制

在GROMACS中，约束（constraints）和限制（restraints）指的是不同的模拟过程。

约束指的是，对力进行积分之后修正键长或键角（或其子集）的大小使其保持不变。GROMACS实现了  
两种主要的约束算法，LINCS/P\-LINCS和SHAKE。

限制具有多种作用，涉及哈密顿量的微扰，以使其产生的系综符合某些预定的条件。限制通常是通过对  
偏离预定的值的项（原子位置，分子内距离和二面角）施加能量惩罚来实现的。冻结组的使用类似。更  
多信息参见手册。

### 3\.10 环境变量

##### GROMACS程序的运行可能会受到环境变量的影响。首先，GMXRC文件中设置的变量对于运行和编译

GROMACS必不可少。以下各节列出了其他一些有用的环境变量。通过在shell中将其设置为任意非空  
的值，大多数环境变量都可以起作用。如果需要设置其他值，请参考下面的具体要求说明。你应该查阅  
自己所用shell的文档，以了解如何为当前使用的shell设置环境变量，或者如何在配置文件中设置环境  
变量以便用于以后的shell。注意，将环境变量导出到批处理控制系统下运行的作业中时，要求各不相同，  
详细信息参阅相应的本地文档。

#### 3\.10\.1 输出控制

##### GMX\_CONSTRAINTVIR 打印约束维里和力维里对应的能量项。

##### GMX\_DUMP\_NL 邻区列表转储级别；默认为 0 。

##### GMX\_MAXBACKUP 当尝试输出同名的新文件时，GROMACS会自动备份旧文件的副本，此变量控制备份

##### 的最大数目，默认为 99 。设置为 0 时，如果已经存在任何输出文件，则无法运行。如果设置为\-1，

##### 会覆盖任何输出文件，不进行备份。

##### GMX\_NO\_QUOTES 如果明确设置了此变量，程序结束时不会打印有趣的名言警句。

##### GMX\_SUPPRESS\_DUMP 当（例如）约束算法失效导致系统崩溃时，不转储每步的文件。

GMX\_TPI\_DUMP 将相互作用能小于此环境变量设定值的所有构型转储到一个 pdb ↪ 614 文件。

GMX\_VIEW\_XPM GMX\_VIEW\_XVG，GMX\_VIEW\_EPS 和 GMX\_VIEW\_PDB 设置的命令分别用于自动查

看 xvg ↪ 623 ， xpm ↪ 620 ， eps ↪ 609 和 pdb ↪ 614 文件类型，默认为xv，xmgrace，ghostview和rasmol。设

置为空可以禁用自动查看特定的文件类型。命令会被分支并在后台运行，优先级别与GROMACS

工具相同（可能不是你想要的效果）。注意不要使用可以阻断终端的命令（如vi），因为可能会运

行多个实例。

GMX\_LOG\_BUFFER 文件I/O的缓冲区大小。设置为 0 时，所有文件I/O都不使用缓冲，因此非常慢。这

对于调试来说非常方便，因为可以确保所有文件始终都是最新的。

GMX\_LOGO\_COLOR 设置 gmx view ↪ 356 徽标的显示颜色。

GMX\_PRINT\_LONGFORMAT 打印十进制数值时使用长浮点格式。

GMX\_COMPELDUMP 仅用于计算电生理学设置（见参考手册↪ 469 ）。初始结构转储到 pdb ↪ 614 文件，这样可以

检查多聚体通道的PBC表示是否正确。

GMX\_TRAJECTORY\_IO\_VERBOSITY 默认为 1 ，打印帧数，例如读取轨迹文件时。设置为 0 则安静运行。

GMX\_ENABLE\_GPU\_TIMING 在日志文件中为CUDA启用GPU计时。注意，CUDA计时在使用多个流时

是不正确的，与区域分解或GPU上的非键和PME类似（这也是它们默认未启用的主要原因）。

GMX\_DISABLE\_GPU\_TIMING 在日志文件中禁用用于OpenCL的GPU计时

#### 3\.10\.2 调试

##### GMX\_PRINT\_DEBUG\_LINES 设置后会打印调试信息对应的行号。

##### GMX\_DD\_NST\_DUMP 将当前DD转储到PDB文件的间隔步数（默认为 0 ）。只在区域分解期间生效，因

此通常应该设为 0 （从不）， 1 \(每个DD阶段\)或 nstlist ↪ 128 的倍数。

GMX\_DD\_NST\_DUMP\_GRID 将当前DD格点转储到PDB文件的间隔步数（默认为 0 ）。只在区域分解期

间生效，因此通常应该设为 0 （从不）， 1 \(每个DD阶段\)或 nstlist ↪ 128 的倍数。

GMX\_DD\_DEBUG 每个区域分解的通用调试触发器（默认为 0 ，表示关闭）。目前只检查全局\-局部原子索

引映射的一致性。

GMX\_DD\_NPULSE 覆盖使用的DD脉冲数（默认为 0 ，表示不覆盖）。通常为 1 或 2 。

GMX\_DISABLE\_ALTERNATING\_GPU\_WAIT 禁用用于等待PME和非键GPU任务完成的专用轮询等待路

径，进行重叠以减少首先到达的力。设置此变量将切换到具有固定等待顺序的通用路径。

在调试中使用了许多这样的额外环境变量，请检查代码\!

#### 3\.10\.3 性能和运行控制

GMX\_DO\_GALACTIC\_DYNAMICS 设置此环境变量可启用行星模拟（只是为了好玩），并允许在 mdp ↪ 612 文

件中设置 epsilon\-r ↪ 132 为\-1。通常， epsilon\-r ↪ 132 必须大于零以防止致命错误。请参阅 网

页↪http://www\.gromacs\.org 上行星模拟的示例输入文件。

GMX\_BONDED\_NTHREAD\_UNIFORM 每个进程的线程数，用于从均匀成键相互作用分布切换到局部成键相

互作用分布；最佳值取决于系统和硬件，默认值为 4 。

GMX\_CUDA\_NB\_EWALD\_TWINCUT 强制使用双程截断内核，使 PP\-PME负载均衡之后 rvdw ↪ 133 等

于 rcoulomb ↪ 132 。会自动切换到双程内核，因此该变量只应该用于基准测试。

GMX\_CUDA\_NB\_ANA\_EWALD 强制使用解析Ewald内核。只应该用于基准测试。

GMX\_CUDA\_NB\_TAB\_EWALD 强制使用表格Ewald内核。只应该用于基准测试。

GMX\_DISABLE\_CUDA\_TIMING 已废弃。请改用GMX\_DISABLE\_GPU\_TIMING。

GMX\_CYCLE\_ALL 运行期间对所有代码进行计时。与线程不兼容。

GMX\_CYCLE\_BARRIER 在每次循环的启动/停止调用之前调用MPI\_Barrier。

GMX\_DD\_ORDER\_ZYX 设置构建区域分解单元的顺序为\(z, y, x\)，而不是默认的\(x, y, z\)。

GMX\_DD\_USE\_SENDRECV2 在约束和虚拟位点通信期间，使用一对MPI\_Sendrecv 调用而不是两个同步

的非阻塞调用（默认为 0 ，表示关闭）。在一些MPI实现中可能会更快。

GMX\_DLB\_BASED\_ON\_FLOPS 基于flop计数进行区域分解的动态负载均衡，而不是基于测量到的时间（默

认为 0 ，表示关闭）。这使得负载均衡可重现，非常有助于调试。该值为 1 时使用flops;值> 1

时会向flops添加\(值\-1\)\*5%的噪声，以增加不均衡性和缩放。

GMX\_DLB\_MAX\_BOX\_SCALING 区域分解负载均衡步骤中允许使用的盒子缩放的最大百分比（默认为 10 ）

GMX\_DD\_RECORD\_LOAD 记录DD负载统计信息，并在运行结束时报告（默认为 1 ，表示打开）

GMX\_DETAILED\_PERF\_STATS 设置后，会将更详细的性能信息打印到 log ↪ 611 文件。输出结果的方式类似

4\.5\.x版本的性能总结，因此对那些使用脚本解析 log ↪ 611 文件或标准输出的人有用。

__GMX\_DISABLE\_SIMD\_KERNELS 禁用与机器架构相关的SIMD优化（SSE2，SSE4\.1，AVX等）的非键内__

__核，强制使用普通的C语言内核。__

__GMX\_DISABLE\_GPU\_TIMING 当时间步长较短时，对异步执行的GPU操作进行计时会产生不可忽略的开__

__销。在这些情况下，禁用计时可以提高性能。__

GMX\_DISABLE\_GPU\_DETECTION 设置后，禁用GPU检测，即使 gmx mdrun ↪ 276 编译时支持GPU。

GMX\_GPU\_APPLICATION\_CLOCKS 将此变量设置为 0 ，ON或DISABLE（不区分大小写）允许禁用CUDA

GPU应用时钟支持。

GMX\_DISRE\_ENSEMBLE\_SIZE 对距离约束系综进行平均时系统的数目。整数值。

GMX\_EMULATE\_GPU 不使用GPU加速函数，而是使用算法等效的CPU引用代码模拟GPU运行。由于

CPU代码很慢，因此仅用于调试。

GMX\_ENX\_NO\_FATAL 在 edr ↪ 609 文件中遇到损坏的帧时禁用退出，允许使用所有帧直到损坏为止。

GMX\_FORCE\_UPDATE 调用mdrun \-rerun时更新力。

GMX\_GPU\_ID 设置方式与mdrun \-gpu\_id相同，GMX\_GPU\_ID 允许用户为不同的进程指定不同的GPU

ID，有助于选择集群中不同计算节点上的不同设备。不能与mdrun \-gpu\_id一起使用。

GMX\_GPUTASKS 设置方式与mdrun \-gputasks 相同，GMX\_GPUTASKS允许对不同的进程，将GPU任

务映射到GPU设备ID的方式不同，例如，MPI运行时允许此变量对于不同进程是不同的。不能

与mdrun \-gputasks一起使用。所有要求与mdrun \-gputasks相同。

GMX\_IGNORE\_FSYNC\_FAILURE\_ENV 允许 gmx mdrun ↪ 276 继续运行，即使文件丢失。

GMX\_LJCOMB\_TOL 设置为浮点值时，覆盖力场浮点参数的默认容差1e\-5。

GMX\_MAXCONSTRWARN 如果设置为\-1，即便产生了太多LINCS警告， gmx mdrun ↪ 276 也不会退出。

GMX\_NB\_GENERIC 使用通用的C内核。如果使用基于组的截断方案并将 GMX\_NO\_SOLV\_OPT 设置为

true，则应该设置此变量，从而禁用溶剂优化。

GMX\_NB\_MIN\_CI 在GPU上运行时使用的邻区列表平衡参数。对于小的模拟系统，设置目标配对列表的

最小数目，可以改进多处理器的负载均衡，从而获得更好的性能。必须设置为非负整数， 0 值会

禁用列表拆分。默认值针对支持的GPU进行了优化，因此正常使用时无需改变，但对于未来的机

器架构可能会有用。

GMX\_NBLISTCG 使用基于电荷组的邻区列表和内核。

GMX\_NBNXN\_CYCLE 设置后，打印详细的邻区搜索循环计数。

GMX\_NBNXN\_EWALD\_ANALYTICAL 强制使用解析Ewald非键内核，与GMX\_NBNXN\_EWALD\_TABLE互斥。

GMX\_NBNXN\_EWALD\_TABLE 强制使用表格Ewald非键内核，与GMX\_NBNXN\_EWALD\_ANALYTICAL互斥。

GMX\_NBNXN\_SIMD\_2XNN 强制使用2x\(N\+N\) SIMD CPU非键内核，与GMX\_NBNXN\_SIMD\_4XN互斥。

GMX\_NBNXN\_SIMD\_4XN 强制使用4xN SIMD CPU非键内核，与GMX\_NBNXN\_SIMD\_2XNN 互斥。

GMX\_NOOPTIMIZEDKERNELS 已废弃，请改用GMX\_DISABLE\_SIMD\_KERNELS。

GMX\_NO\_ALLVSALL 禁用优化的all\-vs\-all内核。

GMX\_NO\_CART\_REORDER 用于初始化区域分解通信器。默认按进程排序，但可以使用此环境变量关闭。

GMX\_NO\_LJ\_COMB\_RULE 在非键内核中强制使用LJ参数查找，而不使用组合规则。

GMX\_NO\_INT ， GMX\_NO\_TERM ， GMX\_NO\_USR1 分别禁用SIGINT，SIGTERM和SIGUSR1的信号处理程序。

GMX\_NO\_NODECOMM 不使用单独的节点间和节点内通信器。

GMX\_NO\_NONBONDED 跳过非键计算；可用于估计将GPU加速器添加到当前硬件设置可能获得的性能增

益\-假设计算足够快，可以在CPU执行成键力和PME计算时完成非键计算。需要冻结粒子以阻

止系统崩溃。

GMX\_PULL\_PARTICIPATE\_ALL 对何时使用单独的牵引MPI通信器（进程数>= 32），禁用默认的探索

方法。

GMX\_NOPREDICT 不预测壳层位置。

GMX\_NO\_SOLV\_OPT 关闭溶剂优化；如果启用了GMX\_NB\_GENERIC会自动进行。

GMX\_NO\_UPDATEGROUPS 关闭更新组。可能允许将小的系统分解为更多区域，代价是更新期间需要更多

的通信。

GMX\_NSCELL\_NCG 每个邻区搜索格点单元的理想电荷组数目被硬编码为 10 。将此环境变量设置为任何

其他整数值会覆盖硬编码的值。

GMX\_PME\_NUM\_THREADS 设置OpenMP或PME线程的数目；覆盖 gmx mdrun ↪ 276 的默认设置；可用于

代替\-npme命令行选项，也可用于设置非统一的每进程/节点线程数。

GMX\_PME\_P3M 使用P3M优化的影响函数，而不是平滑的PME B样条插值。

GMX\_PME\_THREAD\_DIVISION 在所有三个维度上以x y z格式划分PME线程。每个维度上的线程总和

必须等于PME线程的总数（在GMX\_PME\_NTHREADS中设置）。

GMX\_PMEONEDD 如果x和y方向上区域分解单元的数目都设置为 1 ，则对PME进行一维分解。

GMX\_REQUIRE\_SHELL\_INIT 要求初始化壳层位置。

GMX\_REQUIRE\_TABLES 要求使用表格库仑和范德华相互作用。

GMX\_SCSIGMA\_MIN 软核sigma的最小值。注意，此值在 mdp ↪ 612 文件中使用 sc\-sigma ↪ 155 关键字进行

设置，但此环境变量可用于重现4\.5之前版本对于此参数的行为。

GMX\_TPIC\_MASSES 应包含多个质量，用于测试粒子插入到空腔。最后一个原子的质心用于插入空腔。

GMX\_USE\_GRAPH 对成键相互作用使用图表。

GMX\_VERLET\_BUFFER\_RES Verlet截断方案中缓冲区大小的分辨率。默认值为0\.001，但可以使用此环

境变量覆盖。

HWLOC\_XMLFILE 并不是严格意义上的GROMACS环境变量，但在大型机器上，如果你有大量MPI进

程，hwloc检测可能需要几秒钟时间。如果运行hwloc命令lstopo out\.xml，并将此环境变量设

置为此文件的位置，hwloc库将使用缓存的信息，这可能更快。

MPIRUN gmx tune\_pme ↪ 348 使用的mpirun命令。

MDRUN gmx tune\_pme ↪ 348 使用的 gmx mdrun ↪ 276 命令。

GMX\_DISABLE\_DYNAMICPRUNING 禁用动态配对列表修剪。注意， gmx mdrun ↪ 276 仍会将nstlist调整

为假定动态修剪时选择的最佳值。因此，为了获得良好的性能，应使用\-nstlist选项。

GMX\_NSTLIST\_DYNAMICPRUNING 覆盖mdrun探索式选择的动态配对列表修剪间隔。设定值应该介于修

剪频率值（CPU为 1 ，GPU为 2 ）和 nstlist ↪ 128 \- 1之间。

GMX\_USE\_TREEREDUCE 对nbnxn力约化使用树约化。对于大量OpenMP线程的情况可能更快（如果内

存的局部性很重要）。

#### 3\.10\.4 OpenCL 管理

目前，有一些环境变量可用于自定义GROMACS使用的 OpenCL↪https://www\.khronos\.org/opencl/版本的某些  
方面。它们主要与OpenCL内核的运行时编译有关，但也用于设备选择。

GMX\_OCL\_NOGENCACHE 如果设置，则禁用OpenCL内核构建的缓存。缓存通常很有用，方便后面的运行

重用以前运行编译过的内核。目前，在我们解决并发问题之前，始终禁用缓存。

GMX\_OCL\_GENCACHE 启用OpenCL二进制缓存。仅打算用于开发和（专家）测试，因为并发和高速缓存

失效的实现都不安全\!

GMX\_OCL\_NOFASTGEN 如果设置，则生成并编译所有算法风格，否则只生成和编译模拟所需的风格。

GMX\_OCL\_DISABLE\_FASTMATH 防止使用\-cl\-fast\-relaxed\-math编译器选项。

GMX\_OCL\_DUMP\_LOG 如果定义，OpenCL构建日志始终会写入mdrun日志文件。否则，只有在发生错

误时，才会将构建日志写入日志文件。

GMX\_OCL\_VERBOSE 如果定义，则启用OpenCL内核构建的详细模式。目前仅适用于NVIDIA GPU。有

关如何获取OpenCL构建日志的详细信息，请参阅GMX\_OCL\_DUMP\_LOG。

GMX\_OCL\_DUMP\_INTERM\_FILES 如果定义，会将OpenCL构建过程中用到的中间语言代码保存到文件

中。必须关闭缓存才能使此选项生效（请参阅GMX\_OCL\_NOGENCACHE）。

NVIDIA GPU: PTX代码保存在当前目录中，名称为device\_name\.ptx

AMD GPU:为每个构建的OpenCL内核创建\.IL/\.ISA文件。有关在何处创建这  
些文件的详细信息，请查阅\-save\-temps编译器选项的AMD文档。  
GMX\_OCL\_DEBUG 与 OCL\_FORCE\_CPU一起使用或与AMD设备一起使用。它将调试标志添加到编译器  
选项（\-g）中。  
GMX\_OCL\_NOOPT 禁用优化。将cl\-opt\-disable选项添加到编译器选项中。  
GMX\_OCL\_FORCE\_CPU 强制选择CPU设备而不是GPU。仅用于调试。不要指望使用此选项时GROMACS  
能正常运行，这个选项只是用于简化单步执行内核并查看正在发生的情况。  
GMX\_OCL\_DISABLE\_I\_PREFETCH 禁用允许测试的i\-atom数据（类型或LJ参数）预取。  
GMX\_OCL\_ENABLE\_I\_PREFETCH 在允许测试的i\-atom数据（类型或LJ参数）预取不是默认的平台上启  
用此功能。  
GMX\_OCL\_NB\_ANA\_EWALD 强制使用解析Ewald内核。与CUDA环境变量GMX\_CUDA\_NB\_ANA\_EWALD等  
价  
GMX\_OCL\_NB\_TAB\_EWALD 强制使用表格Ewald内核。与CUDA环境变量GMX\_OCL\_NB\_TAB\_EWALD等  
价  
GMX\_OCL\_NB\_EWALD\_TWINCUT 强制使用双程截断内核。与CUDA 环境变量 GMX\_CUDA\_NB\_EWALD\_\-  
TWINCUT等价  
GMX\_OCL\_FILE\_PATH 使用此参数强制GROMACS从自定义位置加载OpenCL内核。只有要覆盖  
GROMACS的默认行为，或者要测试自己的内核时才使用。  
GMX\_OCL\_DISABLE\_COMPATIBILITY\_CHECK 禁用硬件兼容性检查。对开发人员有用，允许在不支持的平  
台（如InteliGPU）上测试OpenCL内核，而无需修改源代码。

#### 3\.10\.5 分析与核心函数

GMX\_QM\_ACCURACY Gaussian程序L510\(MC\-SCF\)模块的精度。

GMX\_QM\_ORCA\_BASENAME tpr ↪ 619 文件的前缀，用于Orca计算的输入和输出文件名。

GMX\_QM\_CPMCSCF 如果设置为非零值，Gaussian QM计算会迭代求解CP\-MCSCF方程。

GMX\_QM\_MODIFIED\_LINKS\_DIR 修改后的Gaussian链接的位置。

DSSP 用于 gmx do\_dssp ↪ 225 ，指向dssp可执行程序（不只是路径，还要包含文件名称）。

GMX\_QM\_GAUSS\_DIR Gaussian的安装目录。

GMX\_QM\_GAUSS\_EXE Gaussian可执行文件的名称。

GMX\_DIPOLE\_SPACING gmx dipoles ↪ 216 使用的间距。

GMX\_MAXRESRENUM 设置 gmx grompp ↪ 252 要重新编号的残基的最大数目。\-1 表示重新编号所有残基。

GMX\_NO\_FFRTP\_TER\_RENAME 一些力场（如AMBER）对于N端和C端残基使用特定的名称（NXXX和

CXXX），像 rtp ↪ 615 条目一样，通常要重命名。设置此环境变量会禁用此类重命名。

GMX\_PATH\_GZIP gunzip可执行文件，用于 gmx wham ↪ 357 。

GMX\_FONT gmx view ↪ 356 程序使用的X11字体的名称。

GMXTIMEUNIT 输出文件中使用的时间单位，可以是fs，ps，ns，us，ms，s，m或h中的任何一个。

GMX\_QM\_GAUSSIAN\_MEMORY Gaussian QM计算使用的内存。

MULTIPROT multiprot可执行文件的名称，用于do\_multiprot程序。

NCPUS Gaussian QM计算使用的CPU数。

GMX\_ORCA\_PATH Orca的安装目录。

GMX\_QM\_SA\_STEP Gaussian QM计算时模拟退火的步长。

GMX\_QM\_GROUND\_STATE 定义Gaussian势能面跳跃计算所用的态。

GMX\_TOTAL total可执行文件的名称，用于do\_shift程序。

GMX\_ENER\_VERBOSE 让 gmx energy ↪ 237 和 gmx eneconv ↪ 234 输出更多信息。

VMD\_PLUGIN\_PATH VMD插件的安装目录。需要能够读取只能由VMD插件识别的文件格式。

VMDDIR VMD安装目录的基准路径。

GMX\_USE\_XMGR 将查看器设置为xmgr（已废弃）而不是xmgrace。

### 3\.11 浮点运算

##### GROMACS始终使用实数进行运算，通常要处理数百万的实数。在计算机中，这些实数以所谓的二

##### 进制浮点表示形式进行编码。这种表示方法有点类似科学计数法（但使用二进制而不是十进制），可

##### 以使得计算速度尽可能快。不幸的是，代数定律只是近似地适用于二进制浮点数。在某种程度上，这

##### 是因为一些简单并能以十进制精确表示的实数（如1/5=0\.2），无法以二进制浮点数精确表示，就像

1/3不能精确地以十进制表示一样。你可以通过搜索引擎找到很多与此相关的详尽讨论，如 维基↪https:  
//en\.wikipedia\.org/wiki/Floating\-point\_arithmetic 以及David Goldberg 1991的论文 What every computer scientist

##### 3\.11\. 浮点运算 69

should know about floating\-point arithmetic （文章↪https://docs\.oracle\.com/cd/E19957\-01/806\-3568/ncg\_goldberg\.html，  
addendum↪https://docs\.oracle\.com/cd/E37069\_01/html/E39019/z400228248508\.html）。Bruce Dawson在他的博客 Random  
ASCII site↪https://randomascii\.wordpress\.com/category/floating\-point/ 上写了许多关于现代浮点编程的文章，这些文章  
非常有价值，值得一读。

因此，对大量以二进制表示的精确十进制数进行求和，所得结果未必等于预期的代数结果或十进制结果。  
在对精确到小数点后两位的部分电荷进行求和时，用户可以观察到这种现象，因为有时所得的总电荷只  
是近似等于整数（但是，如果第一位小数出现了偏差，那就意味着拓扑存在问题）。当GROMACS必须  
在输出中表示这样的浮点数时，有时会使用科学记数法的计算机形式，也称E表示法。在这种表示法中，  
像\-9\.999971e\-01这样的数字实际上是\-0\.9999971，非常接近\-1，对于计算系统的总电荷来说足够了。

让GROMACS基于猜测对数字进行四舍五入是不合适的，因为要进行这样的舍入必须对输入进行一些  
假定，而这些假定不一定真实。相反，用户需要了解工具是如何工作的。

### 3\.12 使用 GROMACS 时的安全性

##### 我们建议GROMACS用户在将未知来源（例如网络）的文件用于GROMACS时要小心。

##### 我们无法保证程序不会出现严重错误而崩溃，这些错误可能会导致执行具有与GROMACS相同权限的

##### 代码，例如删除主目录中的内容。

##### 用户自己创建的文件不会带来这些风险，但在输入错误时可能仍会出现行为异常，崩溃或消耗大量资源

##### 的情况。

##### 从外部获得的运行输入文件应该与来自同一地方的可执行文件需要同样谨慎地对待。

### 3\.13 废弃 GROMACS 功能的策略

##### 有时，功能不再有用，无法修复或维护，或者需要改进其用户接口。开发团队很少这样做。如果没有人

##### 愿意修复，可能会在没有通知的情况下删除损坏的功能。可以工作的功能，只有在上一个主要版本中宣

##### 布了要删除和/或更改之后，才会更改。这样，用户和外部工具提供者通常有一年时间为此类更改做准

##### 备，并联系GROMACS开发人员以了解可能受到的影响以及如何最好地适应这些变化。

##### 在”主分发版本”的注记中，有一个当前预期更改和弃用功能的列表\.

##### 当废弃环境变量被弃用时，用户应确保其脚本根据新版本进行了相应的更新。合理情况下，在完全移除

##### 旧的环境变量之前，开发团队应努力使其在下一额外的版本周期内继续可用。应通过警告告知用户未来

##### 的废弃情况。如果无法保留旧的环境变量或保留旧的环境变量存在很大问题，在一个发布周期内设置已

##### 删除的环境变量应触发警告。

### 3\.14 有用的 mdrun 功能

本节讨论 gmx mdrun ↪ 276 的一些功能，这些功能的说明不太适合放在其他地方。

#### 3\.14\.1 重新运行模拟

使用重新运行功能，你可以提供一个轨迹文件traj\.trr并根据其中的坐标计算系统的物理量，计算时  
使用的物理模型来自 topol\.tpr文件。计算时所用的命令类似 mdrun \-s topol \-rerun traj\.trr。  
所用的 tpr ↪ 619 文件可以与生成轨迹所用的不同。这可用于精确地计算输入坐标的能量或力，或者计算分  
子系统中一部分原子的物理量（参见 gmx convert\-tpr ↪ 203 和 gmx trjconv ↪ 343 ）。与进行 0 步模拟相比，使  
用此功能进行正确的“单点”能量计算更容易。

程序会对轨迹中的每一帧进行邻区搜索，与 nstlist ↪ 128 的值无关，因为 gmx mdrun ↪ 276 不能再对结构  
的生成方法做任何假定。自然，因此也无法使用更新或约束算法。

通常，对于完整模拟期间输出的许多物理量，重新运行功能是无法计算的。它只是将位置作为输入（忽  
略可能存在的速度），并且只计算势能，体积和密度，dH/dl项和限制信息。很明显，它无法计算动能，  
总能量或守恒能量，温度，维里或压力。

#### 3\.14\.2 以可重现的模式运行模拟

##### 通常很难运行一个主要基于浮点运算的，高效的，并行MD模拟，并且使其具有完全的重现性。默认情

况下， gmx mdrun ↪ 276 会根据运行情况适当改变模拟的执行方式，以优化执行性能。但是，使用mdrun  
\-reprod可以启动“可重现模式”的运行方式，这样可以系统地消除运行中所有可能导致无法重现的因  
素；以这种模式，使用相同的输入和硬件重复调用运行会得到二进制相同的结果。但是，即便在这种模  
式下运行，如果使用了不同的硬件，或者不同编译器编译的版本等，结果也无法重现。这种模式通常只  
应在调查可能出现的问题时使用。

#### 3\.14\.3 停止正在运行的模拟

当gmx mdrun收到一个TERM或INT信号时（例如按下Ctrl\+C时），它会在下一个邻区搜索步骤或  
第二次全局通信步骤停止，以较晚者为准。当gmx mdrun收到第二个TERM或INT信号，并且不需  
要保证重现性时，将会在第一次全局通信时停止。在这两种情况下，所有常规输出都将写入文件，并在  
最后一步输出检查点文件。当gmx mdrun收到ABRT信号,或第三个TERM或INT信号时，它将直  
接终止，而不会输出新的检查点文件。使用MPI运行时，只要将信号发送到gmx mdrun的一个进程即  
可，此信号不应发送到mpirun或作为其他进程父进程的gmx mdrun。

#### 3\.14\.4 运行多重模拟

在许多情况下，在同一mdrun调用中运行许多相关的模拟是必要的，有时也很有用。运行副本交换模  
拟就需要这样，就像模拟时使用基于系综的距离或取向限制一样。使用这种方法，运行一系列相关的  
lambda点并计算自由能，也很方便,但要注意与资源利用率和负载均衡有关的潜在副作用,稍后会有讨  
论。

这一功能需要外部 MPI 库，这样才能在模拟集合中进行通信。集合中的n个模拟也可以使用内部MPI  
并行，因此mpirun \-np x gmx\_mpi mdrun中的x是n的倍数，每个模拟会使用x/n个进程。

____3\.14\.____ 有用的 ____mdrun____ 功能 ____71____

运行这类模拟时，有两种组织文件的方法。所有正常机制都可以用于这两种情况，包括\-deffnm。

要启动多重模拟,需要使用 \-multidir选项\.对于多重模拟的输入和输出文件,需要一组n 个子目录，  
每个模拟一个。将所有相关的输入文件都放在目录中（例如命名为topol\.tpr），并使用 mpirun \-np x  
gmx\_mpi mdrun \-s topol \-multidir <目录名> 启动多重模拟。如果多重模拟中的模拟顺序很重要，  
那么当将其提供给\-multidir时，需要对它们的名称进行排序。小心那些对文件名扩展使用字典排序  
的shell，例如：dir1 dir10 dir11 \.\.\. dir2 \.\.\.。

2019:

\-multidir 你必须为 n个模拟创建 n 个目录，通常此选项使用起来最方便。使用组截断方案的gmx

mdrun \-table只能使用这种模式。

\-multi 对n个模拟，每个输入文件的名称后面必须添加从 0 到n\-1的编号（例如topol2\.tpr），然后

使用mpirun \-np x gmx mdrun \-multi n \-s input开始运行。模拟顺序由文件名称中附加的整

数编号决定。

##### 运行多重模拟的示例

mpirun\-np 32 gmx\_mpi mdrun\-multidir a b c d

在 32 个进程启动 4 个模拟。输入和输出文件位于目录a，b，c 和d中。

mpirun\-np 32 gmx\_mpi mdrun\-multidir a b c d\-gputasks 0000000011111111

启动与之前相同的多重模拟。机器有两个物理节点，每个节点两个GPU，这样每个节点会有 16 个MPI  
进程，每个模拟使用 8 个MPI进程。一个节点使用 16 个MPI进程进行PP计算，这些进程被映射到  
ID为 0 和 1 的GPU，即使它们来自多个模拟。它们按指示的顺序进行映射，这样每个模拟的PP进程  
使用单个GPU。但是，按照 0101010101010101 顺序可以运行得更快。

##### 运行副本交换模拟

运行多重模拟时，使用 gmx mdrun \-replex n意味着每隔指定步数尝试进行一次副本交换。副本的数  
目由\-multidir选项指定，如上所述。所有运行输入文件使用的耦合参数值（如温度）都应该不同，这  
些参数随输入文件的顺序依次增加。副本交换的随机种子由\-reseed指定。每次交换之后，会缩放速  
度并进行邻区搜索。有关GROMACS中副本交换功能的更多详细信息，见参考手册↪ 469 。

##### 多重模拟性能的考虑

##### 多重模拟之间的通信频率会影响性能,具体与算法高度相关，但一般情况下，建议在设置多重模拟时尽

##### 可能减少模拟间通信的频率，但也要视需要而定。不过，即使多重模拟成员间通信不频繁（或根本不通

##### 信），因而相关的性能开销很小甚至可以忽略不计，负载不均衡仍会对性能和资源利用率产生显著影响。

##### 当前的多重模拟算法使用固定的间隔进行数据交换（例如，每隔 N步进行一次副本交换），因此多重模

##### 拟的所有成员都需要在达到这一步后才能进行集体通信，然后其中的任何一个成员都可以进入N\+1步。

##### 因此，多重模拟中最慢的成员会决定整体的性能。这种负载不均衡不仅会限制性能，还会造成资源闲置；

例如，对于一个n路多重模拟,如果其中的一个模拟运行速度只有其余模拟的一半，那么分配给运行速度  
较快的n\-1个模拟的资源就会闲置，闲置时间约为整个多重模拟任务挂钟时间的一半。造成这种不均衡  
的原因可能是多重模拟中各模拟之间固有的工作量不平衡，也可能是硬件速度的差异,或节点间网络性  
能的变化影响了部分进程，因而只影响了部分模拟。要减少闲置的资源量，就必须减少负载不均衡，这

##### 72 第 3 章 用户指南

##### 可能涉及拆分不通信的多重模拟，或确保在集群上请求”紧凑”分配（如果作业调度系统允许的话）。注

##### 意，不均衡也适用于像FEP计算这样的非通信多重模拟，因为在整个MPI任务完成之前，较早完成的

##### 模拟占有的资源无法收回。

#### 3\.14\.5 控制模拟的长度

通常，最好通过 mdp ↪ 612 选项 nsteps ↪ 125 来管理MD模拟的长度，但有些情况下可能需要更多的控制。  
gmx mdrun \-nsteps 100可以覆盖 mdp ↪ 612 文件中的设置并运行 100 步。gmx mdrun \-maxh 2\.5会在  
时间快要达到2\.5小时时终止模拟，当使用集群队列运行时这个选项很有用（只要排队系统不会挂起模  
拟）。

#### 3\.14\.6 运行膜蛋白嵌入模拟 2019

##### 这个模块可用于将膜蛋白嵌入到一个平衡好的脂质双层中，用户可以指定膜蛋白的位置和方向。

所用的方法最初称为ProtSqueeze技术（Yesylevskyy S\.O\., J\. Chem\. Inf\. Model 47\(5\) \(2007\) 1986\-

\(^94\) ↪https://dx\.doi\.org/10\.1021/ci600553y），后来GROMACS在 g\_membed 工具中实现这种方法（Wolf et al,  
J\. Comp\. Chem\. 31 \(2010\) 2169\-2174↪http://onlinelibrary\.wiley\.com/doi/10\.1002/jcc\.21507/full）。目前，如果指定了  
\-membed选项（见下文），就可以在mdrun中使用g\_membed的功能。这种使用方式不太合适，将来可  
能被废弃，并使用单独的程序，如gmx membed 来完成膜蛋白的嵌入。  
这种方法的主要优点在于，可以使用非常复杂的脂质双层，其中包含许多不同的组分，而且这些组分已  
经在先前的模拟经过了很长时间的弛豫。理论上讲，可以通过类似于 gmx solvate ↪ 328 的流程进行嵌入，  
但由于脂质比水分子大得多，如果我们只是简单地去除有原子发生重叠的所有脂质分子，就会导致在蛋  
白质和膜之间形成很大的真空层。相反，这个模块的工作原理是，首先在xy平面中人工收缩蛋白质，形  
成一个远小于原来的蛋白核，然后去除与这个蛋白核重叠的脂质，在此之后我们逐渐将蛋白质原子恢复  
到其初始位置，同时对系统的其余部分进行常规的动力学模拟，以使脂质适应蛋白质。  
要使用膜嵌入功能，首先要建立一个脂质双层，它在xy平面中大小略大于你最终需要的尺寸，并确保  
在膜外有足够的水来容纳球状结构区域。将蛋白质放置到与脂质双层相同的坐标（和拓扑）文件中，并  
确保其位于双层的中间，取向和位置符合要求。  
必须在控制模拟的mdp文件中输入第一个设置。你需要一个与蛋白质对应的能量组，并将这个组（在  
所有维度上）冻结，我们应该排除蛋白质内部的所有相互作用，以避免它变形时出现问题。例如：  
integrator =md  
energygrps =Protein  
freezegrps =Protein  
freezedim =Y Y Y  
energygrp\_excl=Protein Protein  
你还需要对实际的膜嵌入过程进行一些设置。将它们作为相似的名称和值配对输入，但在单独的文本数  
据文件embed\.dat中，需要提供 \-membed选项的参数（在解释该过程时，我们参考下面的内容）。嵌  
入过程分为 4 个阶段：  
1\.蛋白质围绕其质心的大小会进行调整，xy平面（双层平面）的大小调整因子为xy，z轴（垂直于  
双层）方向的大小调整因子为z。如果蛋白质的高度等于或小于膜的厚度，那么对z方向使用大  
于1\.0的大小调整因子可以防止蛋白质被脂质包裹住。  
2\.与大小调整后的蛋白质有重叠的所有脂类和溶剂分子都会被去除。关闭蛋白质内部的所有相互作

用，以防止使用很小的大小调整因子时可能出现的数值问题。

3\.进行一步md，系统其余部分的原子会移动。

4\.大小调整因子按\(1\-xy\)/nxy和\(1\-z\)/nz进行小的调整，其中nxy和nz 为需要使用的迭代次数。

程序会首先调整xy平面的大小调整因子因子。直到xy平面的大小调整因子为1\.0（经过nxy迭

代）之后，z方向的大小调整因子才会改变。

5\.重复步骤 3 和 4 ，直到蛋白质再次达到其原始大小，即进行nxy\+nz此迭代之后。嵌入后，你可能

仍然需要进行一个短时间的弛豫。

可以在embed\.dat文件中指定参数，如果省略设置，会使用默认值：

xyinit\(0\.5\)开始嵌入之前，xy平面中蛋白质的大小调整因子。

xyend\(1\.0\) xy平面内最终的大小调整因子。

zinit\(1\.0\)开始嵌入之前，z方向蛋白质的大小调整因子。

zend\(1\.0\) z方向最终的大小调整因子。

nyx\(1000\) xy平面内的迭代次数。

nz\(0\) z方向的迭代次数。

rad\(0\.22\)探针半径，用于检查嵌入组和膜之间是否重叠。

pieces\(1\)进行分段调整大小。选择待插入组的一部分，并根据它们自身的几何中心调整其大小。

asymmetry\(no\)允许不对称插入，即不检查从上层膜和下层膜去除的脂质分子的数目。

ndiff\(0\)从下层膜（指定负数）或上层膜（指定正数）额外去除的脂质分子的数目。

maxwarn\(0\)允许的嵌入警告的最大数目。

### 3\.15 提高 mdrun 的性能

##### 这里我们给出GROMACS所用的并行化和加速技术的一个概述。目的是帮助理解那些使得GROMACS

##### 成为最快的分子动力学程序之一的基本机制。所提供的信息会有助于选择适当的并行化选项，运行配置

##### 以及加速选项，以实现最佳模拟性能。

GROMACS构建系统和 gmx mdrun ↪ 276 工具有很多内置和可配置的功能，可用于检测你的硬件并非常高  
效地使用它们。对于很多随意和认真的使用来说， gmx mdrun ↪ 276 自动选择的运行设置已经足够好了。  
但是，为了最大限度地利用硬件，最大限度地提高科学研究的质量，请继续阅读\!

#### 3\.15\.1 硬件的背景信息

##### 现代计算机硬件复杂而且异构，因此我们需要讨论一些背景信息，并建立一些定义。经验丰富的HPC

##### 用户可以跳过本节。

##### 核实际执行指令的硬件计算单元。一个处理器中通常会有超过一个的核，常常会有很多个核。

##### 高速缓存一种特殊的内存，是核的局部存储器，访问速度比主内存快得多。高速缓存与主内存的关系有

##### 点类似我们的桌面与档案柜。通常每个核会有几层与其相关的缓存。

##### 插槽共享某种局部性的一组核，例如共享缓存。这使得在同一插槽内的核上分配计算工作比在不同插

##### 槽的核上分配计算工作更高效。现代处理器通常有多个插槽。

##### 节点一组共享较大级别局部性的插槽，例如无需任何网络硬件即可共享访问同一内存。普通的笔记本

##### 电脑或台式电脑就是一个节点。节点通常是用户可以请求使用的大型计算集群中的最小单元。

##### 线程核执行的指令流。有许多不同的编程抽象模式可以创建和管理多个线程上的计算分配，例如

OpenMP，pthreads，winthreads，CUDA，OpenCL和OpenACC。某些硬件可以将多个软件线程

映射到一个核；在Intel x86处理器上，这称为“超线程”，而更一般的概念通常称为SMT，即“同

时多线程”。例如，IBM Power8每个核最多可以使用 8 个硬件线程。此功能通常可以在硬件BIOS

中启用或禁用，也可以通过Linux操作系统中的设置启用或禁用。GROMACS通常可以利用这一

点，不费代价便可获得适度的性能提升。在大多数情况下，默认会启用它，例如在新的x86处理

器上默认就会启用，但在某些情况下，系统管理员可能禁用了此功能。如果出现这种情况，请询问

管理员看能够为你重新启用。如果你不确定是否已启用，请检查日志文件中输出的CPU信息，并

与网上查找到的CPU规格进行比较。

线程关联（绑定）默认情况下，大多数操作系统都允许软件线程在核（或硬件线程）之间进行迁移，以

自动帮助平衡工作负载。但是，如果允许这样做的话， gmx mdrun ↪ 276 的性能可能会变差，特别是

在依赖于进程内的多线程时，性能会急剧下降。为避免这种情况， gmx mdrun ↪ 276 默认会设置其线

程与各个核/硬件线程的关联性，除非用户或软件环境已经这样做（或者并不是整个节点都用于运

行，即存在节点共享的可能性）。设置线程关联有时称为线程“绑定”。

____MPI \(Message Passing Interface\)____

占主导地位的多节点并行方案，它提供了一种标准化的语言，可以使用这种语言编写跨多个节点

的程序。

秩号在MPI中，秩号是多节点并行方案中使用的最小硬件分组。此分组可以由用户控制，并且可以对

应于核，插槽，节点或一组节点。最佳选择取决于硬件，软件和计算任务。有时MPI秩号也称为

MPI进程。

GPU 一种图形处理单元，对于特定类型的计算工作负载，它通常比传统处理器更快，更高效。GPU始

终与特定节点相关联，并且通常与该节点内的特定插槽相关联。

OpenMP 许多编译器都支持的一种标准化技术，用于在多个核上共享计算工作负载。通常与MPI结

合以实现MPI/OpenMP混合并行。

CUDA 由NVIDIA开发的专有并行计算框架和API，定位于其加速器硬件。GROMACS使用CUDA

为NVIDIA硬件提供GPU加速。

OpenCL 一种基于开放标准的并行计算框架，由基于C99的编译器和针对异构硬件和加速器硬件的编

程API组成。GROMACS在AMD设备（包括GPU和APU）, Intel集成GPU,和Apple Silicon

集成GPU,上使用OpenCL进行GPU加速；还支持一些NVIDIA硬件。GROMACS新版本中，

OpenCL已被弃用，转而使用SYCL。

____SYCL____

基于C\+\+17的开放标准，用于异构系统。SYCL有多种实现，其中 GROMACS支持其中

的两种：Intel oneAPI DPC\+\+↪https://www\.intel\.com/content/www/us/en/developer/tools/oneapi/dpc\-compiler\.html 和

hipSYCL↪https://github\.com/illuhad/hipSYCL。在AMD和Intel GPU上GROMACS使用SYCL进行

GPU加速。也试验性地支持NVIDIA GPU。

SIMD 一种CPU指令类型，通过这种指令，现代CPU核可以在一个周期内执行多个浮点指令。

3\.15\. 提高 mdrun 的性能 75

#### 3\.15\.2 GROMACS 中并行化的工作目录

在涉及如何充分利用硬件时， gmx mdrun ↪ 276 中的算法及其实现是最相关的。详细信息见参考手册↪ 469 。  
其中最重要的是

区域分解区域分解（DD）算法将非键相互作用的（短程）部分分解到共享空间局部性的区域，从而可  
以使用高效的算法。每个区域处理其成员的所有粒子\-粒子（PP）相互作用，并映射到单个MPI  
进程。在PP进程中，OpenMP线程可以共享工作负载，并且可以将一些工作转移到GPU上。PP  
进程还处理其区域成员的任何成键相互作用。一块GPU可以用于多个PP进程，但通常最高效的  
方式为，每块GPU只使用一个PP进程，并且该进程具有数千个粒子。当在CPU上完成PP进  
程工作时， mdrun ↪ 276 会大量使用核心的SIMD功能。有各种命令行选项↪ 78 来控制DD算法的行  
为。

粒子网格 ____Ewald____ 粒子网格Ewald（PME）算法处理非键相互作用的长程部分（库仑，可能也包括  
Lennard\-Jones）。要么全部，要么只有一部分进程可以参与长程相互作用的计算工作（通常不准确  
地简称为PME部分）。因为该算法使用了需要全局通信的3D FFT，所以其并行效率会随着参与  
进程的增多而变得更糟，这可能意味着只使用一部分进程是最快的（例如，使用四分之一到二分之  
一的进程）。如果有单独的PME进程，那么其余的进程可以处理PP工作。否则，所有进程都会  
进行PP和PME工作。

#### 3\.15\.3 并行化方案

GROMACS以性能为导向，非常注重高效的并行化。有多种可用的并行化方案，因此在给定的硬件上，

运行模拟时可以选择不同的运行配置。

通过 SIMD 进行内核并行化： SSE ， AVX 等

GROMACS提供的一种性能改进方式是通过使用 单指令多数据（SIMD）指令。详细信息请参见安装

指南中的 SIMD 支持↪ 14 。

在GROMACS中，通过使用特定于硬件的SIMD内核，可以将SIMD指令用于对并行化性能影响最

大的代码部分（非键力和成键力的计算，PME和邻区搜索）。这构成了可用的三种非键内核级别之一：

参考或通用内核（慢但可用于生成测试的参考值），优化的纯C内核（可跨平台使用，但仍然很慢）和

SIMD内在加速内核。

SIMD内在代码由编译器编译。从技术上讲，可以将不同级别的加速代码编译进一个二进制文件中，但

这样做的话在代码的许多部分中都很难管理加速。因此，你需要为目标CPU的SIMD功能配置和编

译GROMACS。默认情况下，构建系统会检测执行编译的主机所支持的最高加速。在具有不同最高

SIMD指令集的机器上进行交叉编译，为设置目标加速，可以使用CMake选项\-DGMX\_SIMD。要在多台  
不同的机器上使用单个安装，可以使用最低的通用SIMD指令集编译分析工具（因为这些工具基本不  
依赖SIMD加速），但是为了获得最佳性能，应该使用目标架构的最高（最新）nativeSIMD指令集  
对 mdrun ↪ 276 进行单独编译（GROMACS支持）。

最近的Intel CPU架构在CPU的最大时钟频率（即速度）以及它执行的SIMD指令的宽度（即给定  
速度下的吞吐量）之间进行了权衡。特别是，IntelSkylake和Casade Lake处理器（例如，Xeon SP  
Gold/Platinum）使用更窄的SIMD时可以提供更好的吞吐量，因为它具有更好的时钟频率。考虑使用  
GMX\_SIMD=AVX2\_256而不是 GMX\_SIMD=AVX512 来配置构建 mdrun ↪ 276 ，以便在GPU加速或高度并行  
的MPI运行中获得更好的性能。

一些基于ARM的最新CPU（如Fujitsu A64fx）支持可伸缩向量扩展（SVE, Scalable Vector Exten\-

sions）。虽然SVE可用于生成相当高效的向量长度无关（VLA, Vector Length Agnostic）代码，但并不

适合GROMACS（因为SIMD向量长度假定在CMake时已知）。因此，在CMake时必须固定SVE向量

长度。默认情况下是在CMake时自动检测默认的向量长度（通过the/proc/sys/abi/sve\_default\_\-

vector\_length伪文件），可以通过GMX\_SIMD\_ARM\_SVE\_LENGTH=<len>进行配置。支持的向量长度为

128 、 256 、 512 和 1024 。由于SIMD短程非键内核对于每个SIMD向量最多只能支持 16 个浮点数，因

此 1024 位向量长度只适用于双精度（例如：\-DGMX\_DOUBLE=on）。请注意，即使mdrun在运行时检查

了SIMD向量长度，使用与CMake时设定长度不同的向量运行也是未定义的行为，mdrun可能会在检

查之前崩溃（会以用户友好的错误信息中止）。

##### 通过 OpenMP 进行进程（处理器）级别的并行化

GROMACS mdrun ↪ 276 支持OpenMP多线程，可用于所有代码\(对 2019 版,则可用于 Verlet 截断方

案↪ 45 的所有代码，以及组方案中的PME代码\)。默认启用OpenMP，要打开/关闭它，可以在配置时使

用CMake变量GMX\_OPENMP，在运行时使用\-ntomp选项（或OMP\_NUM\_THREADS环境变量）。OpenMP

的实现非常高效，扩展性很好，在Intel机器上最多可使用12\-24个线程，在AMD CPU上最多可使用

6\-8个线程。

##### 通过 GPU 卸载和线程 MPI 进行节点级并行化

##### 使用线程 MPI 进行多线程

线程MPI库基于系统的线程支持实现MPI 1\.1规范的子集。它同时支持POSIX p线程和Windows线  
程，从而为大多数Unix/Linux和Windows操作系统提供了极大的可移植性。作为MPI的替代品，线  
程MPI可以在单台机器上（即不通过网络）编译和运行 mdrun ↪ 276 ，而无需MPI。此外，它不仅提供了  
使用多核CPU计算机的快捷方式，而且在某些情况下线程MPI还可以使得 mdrun ↪ 276 的运行速度略快  
于MPI。  
GROMACS源代码中包含了线程MPI，它是默认的并行模式，实际上使得串行 mdrun ↪ 276 被废弃了。可  
以使用CMake变量GMX\_THREAD\_MPI来控制使用线程MPI进行编译。  
线程MPI兼容大多数 mdrun ↪ 276 功能和并行化方案，包括OpenMP，GPU;但不兼容MPI和多重模拟  
运行。  
默认情况下，线程MPI的mdrun会使用机器的所有可用内核，方法是启动适当数量的进程或OpenMP  
线程来占用所有内核。进程数目可以使用\-nt和\-ntmpi选项进行控制。\-nt表示要使用的总线程数  
（可以是线程MPI和OpenMP线程的混合,对于 2019 版,只适用于 Verlet 截断方案↪ 45 ）。

##### 混合 / 异构加速

混合加速意味着在可用CPU和GPU之间分配计算工作，以提高模拟性能。为了在CPU和GPU上实

现高效加速，我们开发了新的非键算法根据\(对 2019 版,只适用于 Verlet 截断方案↪ 45 \)。

模拟计算密集程度最高的部分，非键力计算,以及可能的PME,成键力计算,更新,约束都可以卸载到

GPU上，并与剩余的CPU工作同时执行。GROMACS中的大多数常用算法都支持原生GPU加速\.有

关GPU内核的更多信息，请参阅安装指南↪ 8 。

2019:使用PME，反应场和普通截断静电的 Verlet 截断方案↪ 45 支持原生GPU加速（不适用于组方案）。

原生GPU加速可以打开或关闭，方法是，在运行时使用 mdrun ↪ 276 \-nb选项，或者在配置时使用CMake

变量GMX\_GPU。

为了有效地使用所有可用的计算资源，CPU和GPU计算是同时进行的。当CPU使用OpenMP多线

程计算成键力和PME长程静电的同时，GPU计算非键力。借助区域分解，可以支持单个节点以及跨多

个节点上的多个GPU。单个GPU会分配给一个区域的非键工作负载，因此，使用的GPU数必须与模

拟开始时的MPI进程数（或线程MPI的线程数）匹配。可用的CPU核心会在进程（或线程MPI线

程）之间进行划分，一组带有GPU的核心会在各自的区域上执行计算。

使用PME静电时， mdrun ↪ 276 支持自动CPU\-GPU负载均衡，方法是将工作负载从CPU上完成的

PME网格计算转移到GPU上完成的粒子\-粒子非键计算。启动时，在前 100 到 1000 个MD步中会执

行几次迭代进行调整。这些迭代涉及缩放静电截断和PME格点间距，以便能提供最佳的CPU\-GPU负

载均衡。使用 mdp ↪ 612 选项 rcoulomb ↪ 132 =rvdw提供的值表示调整开始时的最小静电截断值，因此应该

选择尽可能小的值（但对于实际模拟仍然合理）。Lennard\-Jones截断值rvdw保持固定。我们不允许将

其缩放到更短的截断值，因为我们不想更改rvdw，并且这么做不会提升性能\(2019版的对于Verlet截

断方案来说\)。

虽然自动CPU\-GPU负载均衡总会尝试找到最佳的截断设置，但它无法保证始终都能平衡CPU和GPU

工作负载。当CPU线程计算成键力和PME的速度大于GPU计算非键力的速度时，即便使用尽可能

短的截断，也会发生负载不均衡的情况。在这种情况下，CPU会等待GPU，花费的时间会写入日志文

件末尾的周期和记时汇总表，标记为Wait GPU NB local。

##### 通过 MPI 在多个节点上并行

GROMACS中MPI并行化的核心是具有动态负载均衡的电中性区域的区域分解↪ 76 。要在多台机器

（例如集群的节点）上进行并行化模拟， mdrun ↪ 276 需要使用MPI进行编译，这可以使用CMake变量  
GMX\_MPI启用。

##### 控制区域分解算法

##### 本节列出了影响区域分解算法的选项，它们涉及如何将工作负载分解到可用的并行硬件。

\-rdd 可用于设置电荷组间的成键相互作用所需的最大距离。非键截断距离以下的两体成键相互作用的

通信，总是与非键通信一起进行的，没有其他通信成本。超出非键截断范围的粒子只有在缺少成键

相互作用时才会进行通信；这意味着额外的通信成本很小，几乎与\-rdd的值无关。通过动态负

载均衡，\-rdd选项还设置区域分解单元大小的下限。默认情况下，\-rdd由 gmx mdrun ↪ 276 根据

初始坐标确定。所选值会在相互作用范围和通信成本之间进行平衡。

\-ddcheck 默认启用。当电荷组之间的成键相互作用超出成键截断距离时， gmx mdrun ↪ 276 会终止并显

示错误信息。对于不生成排除的配对相互作用和表格键，可以使用\-noddcheck选项关闭此检查。

\-rcon 当存在约束时，\-rcon选项也会影响单元大小的极限。通过NC个约束连接的粒子，其中NC

为LINCS阶数加 1 ，不应超出最小单元大小。发生这种情况时会生成错误信息，用户应更改分解

或减少LINCS阶数，并增加LINCS迭代次数。默认情况下 gmx mdrun ↪ 276 会以保守的方式估计

P\-LINCS所需的最小单元大小。在高并行化的情况下，使用\-rcon设置P\-LINCS所需的距离会

很有用。

\-dds 使用动态负载均衡时，设置单元可以使用的最小x，y和/或z缩放。 gmx mdrun ↪ 276 会确保单元

至少按此因子缩小。此选项用于自动空间分解（不使用\-dd时）以及确定格点脉冲数，而格点脉

冲数又设置了允许的最小单元大小。在某些情况下，可能需要调整\-dds的值，以考虑系统高或

低的空间不均匀性。

多级并行化： ____MPI____ 和 ____OpenMP____

CPU开发中的多核趋势证实了多级并行化的必要性。当前的多处理器计算机可以有2\-4个CPU，核心  
数高达 64 个。由于内存和缓存子系统越来越落后于多核的演进，这就增加了非一致内存访问（NUMA）  
效应，它可能成为性能瓶颈。同时，所有核心共享一个网络接口。在纯MPI并行方案中，所有MPI进  
程都使用相同的网络接口，尽管MPI节点内通信通常效率很高，但节点间的通信可能会成为并行化的  
限制因素。对于使用PME（通信密集型）和通过慢速网络连接的“胖”节点的高度并行模拟，情况尤其  
明显。多级并行旨在通过采用有效的节点内并行，通常是多线程，来解决NUMA和通信相关的问题。

将OpenMP与MPI相结合会产生额外的开销，尤其是运行单独的多线程PME进程时。根据机器架构，  
输入系统的大小以及其他因素，MPI\+OpenMP运行对于少量进程已经够快而且更快（例如多处理器的  
Intel Westmere或Sandy Bridge），但也可能相当慢（例如多处理器的AMD Interlagos机器）。然而，在  
高度并行的运行中，多级并行有一个更明显的优势。

##### 单独的 PME 进程

##### 在CPU进程上，粒子\-粒子（PP）和PME计算是在同一过程中相继进行的。PME需要全面的全局通

##### 信，在大多数情况下这是扩展到大量内核时的限制因素。通过指定一些只进行PME计算进程，可以极

##### 大地提高并行的性能。

PME进程中也可以使用OpenMP多线程\(2019版的组截断方案和Verlet截断方案都支持这种做法\)。  
在PME中使用多线程在高并行化时可以提高性能。其原因在于，当使用N>1个线程时，通信的进程  
数量以及消息数量会减少N的一个因子。但请注意，现代通信网络可以同时处理多个消息，这样使用更  
多进程通信可能会有利。

低并行化时不会使用单独的PME进程，但在并行化较高时会自动使用（大于 16 个进程）。PME进程的  
数目由mdrun估计。如果PME负载高于PP负载，mdrun会自动平衡负载，但这会导致额外的（非  
键）计算。这避免了大部分进程的闲置；通常有3/4的进程是PP进程。但为了确保高度并行运行的最  
佳绝对性能，建议调整此数字，也可以使用 tune\_pme ↪ 348 工具自动调整。

PME进程的数目可以通过 \-npme选项在 mdrun ↪ 276 命令行中手动设置，PME线程的数目可以在命令  
行中使用\-ntomp\_pme选项指定，或者使用GMX\_PME\_NUM\_THREADS 环境变量来指定。在具有不同核数  
的计算节点上运行时后一方法特别有用，因为它可以在不同节点上设置不同数目的PME线程。

#### 3\.15\.4 在单个节点上运行 mdrun

gmx mdrun ↪ 276 可以用几种不同的方式进行配置和编译，以便在单个节点上可以高效地运行。默认配置  
使用了合适的编译器，会部署多级混合并行机制，使用CUDA，OpenMP和硬件原生线程平台。为了方  
便编程，在GROMACS中，那些原生线程用于在单个节点上实现与节点之间使用的MPI方案相同的  
MPI方案，但效率更高；这称为线程MPI。从用户角度来看，真正的MPI和线程MPI看起来几乎相  
同，并且除非另有说明，GROMACS所指的MPI进程可以是这两种类型中的任意一种。 gmx mdrun ↪ 276  
也可以在单个节点内使用真正的外部MPI，但运行速度要比线程MPI版本慢。

默认情况下， gmx mdrun ↪ 276 在运行时会检查可用的硬件，并尽量高效地使用整个节点。日志文件，标  
准输出（stdout）和标准错误（stderr）用于打印诊断信息，通知用户所做的选择以及可能的后果。

有许多命令行参数用于修改默认行为。

\-nt 要使用的总线程数。默认值 0 ，会启动与可用核心一样多的线程。线程是否为线程MPI进程，

和/或这些进程中的OpenMP线程取决于其他设置。

\-ntmpi 要使用的线程MPI进程总数。默认值 0 ，会从每个GPU（如果存在）启动一个进程，否则每

个核一个进程。

\-ntomp 每个进程启动的OpenMP线程总数。默认值 0 ，会在每个可用核心上启动一个线程。或者，如

果设置了的话， mdrun ↪ 276 会使用系统环境变量（如 OMP\_NUM\_THREADS）指定的值。请注意，出

于效率原因，OpenMP线程的最大数目（每个进程）限制为 64 个。虽然使用高于此数的线程好处

很少，但可以使用CMake变量GMX\_OPENMP\_MAX\_THREADS来增加最大限制的数目。

\-npme 如果使用，指定专用于计算PME长程部分的总进程数。默认值\-1，只在线程总数至少为 12 时

才会使用专门用于PME的进程，并且会使用大约四分之一的进程用于长程部分的计算。

\-ntomp\_pme 当PME计算中使用单独的PME进程时，每个单独的PME进程中OpenMP线程的总

数。默认值 0 ，使用\-ntomp 的值。

\-pin 可以设置为 auto，on 或off，控制 mdrun ↪ 276 是否尝试设置线程与核的关联。默认为auto，

这意味着 mdrun ↪ 276 如果检测到节点上的所有核都用于 mdrun ↪ 276 ，那么其行为类似on，并尝试设

置关联性（除非它们已被其他选项设定）。

\-pinoffset 如果\-pin on，则指定逻辑核心编号， mdrun ↪ 276 会将第一个线程关联到该核心。当在一

个节点上运行多个 mdrun ↪ 276 实例时，使用此选项可以避免将来自不同 mdrun ↪ 276 实例的线程关联

到同一个核心。

\-pinstride 如果\-pin on，则指定核的逻辑核心编号的增量， mdrun ↪ 276 会将其线程关联到这些核上。

当在一个节点上运行多个 mdrun ↪ 276 实例时，使用此选项可以避免将不同 mdrun ↪ 276 实例的线程关

联到同一个核上。使用默认值 0 可以最大限度地减少每个物理核的线程数，这样 mdrun ↪ 276 可以

管理特定于硬件，操作系统和配置的详细信息，这些信息与如何将逻辑核心映射到物理核心有关。

\-ddorder 可以设置为 interleave，pp\_pme 或cartesian。默认为 interleave，这意味着任何单

独的PME进程将按照PP，PP，PME，PP，PP，PME等顺序映射到MPI进程。这样做通常

可以最大限度地利用可用的硬件。pp\_pme首先映射所有PP进程，然后再映射所有PME进程。

cartesian是一种特殊用途的映射，通常只用于特殊的环形网络，它们具有加速的全局通信器用

于笛卡尔通信。如果没有单独的PME进程，此选项不起作用。

\-nb 用于设置执行短程非键相互作用的设备。可以设置为auto，cpu，gpu。默认为auto，如果可用，

则使用兼容的GPU。设置为cpu则要求不使用GPU。设置为gpu则需要有一个兼容的GPU可

用，并会使用它。

\-pme 用于设置执行长程非键相互作用的设备。可以设置为auto，cpu，gpu。默认为auto，如果可

用，则使用兼容的GPU。设置为gpu则需要有一个兼容的GPU可用。GPU上的PME不支持

多个PME进程，因此如果使用GPU进行PME计算，则\-npme必须设置为 1 。

\-bonded 用于设置执行成键相互作用的设备，这些相互作用的计算是区域PP工作负载的一部分。可

以设置为auto，cpu，gpu。默认为auto，只在可用时使用兼容的CUDA GPU，GPU处理短

程相互作用的计算工作，CPU处理长程相互作用的计算工作（静电或LJ）。成键相互作用的计算

工作所用的GPU与短程相互作用的相同，并且不能单独分配。设置为gpu则需要有一个兼容的

GPU可用，并会使用它。

____\-update____

用于设置在何处执行更新和约束,如果存在的话。可设置为auto、cpu、gpu。默认设置为auto，

意味着当前始终使用CPU。设置为gpu需要有兼容的CUDA GPU可用，模拟使用单个进程。

GPU上的更新和约束目前不支持质量和约束的自由能微扰、区域分解、虚拟位点、Ewald表面校

正、副本交换、约束牵引、取向限制和计算电生理学。

\-gpu\_id 一个字符串，指定可供每个节点上的进程使用的GPU的ID号。例如， 12 指定ID为 1

和 2 的GPU（ID由GPU运行时报告获知）可用于 mdrun ↪ 276 。在与其他计算共享节点时，或者

GROMACS不能使用那些专门用于显示的GPU时，这非常有用。如果不指定此参数， mdrun ↪ 276

会使用所有的GPU。如果存在多个GPU，可以使用逗号隔开ID，因此12,13 表示GPU 12和

13 可用于 mdrun ↪ 276 。如果需要在模拟的不同节点上使用不同的GPU，可以对不同节点上的进程

设置不同的环境变量GMX\_GPU\_ID，这样就能达到目的。在GROMACS 2018之前的版本中，此参

数用于同时指定GPU可用性和GPU任务分配。后者现在是通过\-gputasks 参数完成的。

\-gputasks 一个字符串，指定此节点上相应的GPU任务所使用的GPU的ID号。例如， 0011 指定

前两个GPU任务使用GPU 0，而另外两个任务使用GPU 1。当使用此选项时， mdrun ↪ 276 必须

知道进程的数目，以及应该在何处运行不同类型的任务，例如使用\-nb gpu，解析映射时只会考

虑设置为在GPU上运行的任务。详细信息，请参阅将任务分配给 GPU ↪ 90 。注意，\-gpu\_id和

\-putasks不能同时使用\!在GROMACS 2018之前的版本中，只有单一类型的GPU任务（PP）

才可以在任何进程上运行。现在已经对在GPU上运行PME提供了一些支持，那么对于单进程模

拟，GPU任务的数目（以及\-gputasks字符串所预期的GPU ID的数目）实际上可以是 3 。在这

种情况下，ID仍然必须相同，因为单个进程使用多个GPU尚未实现。字符串中每个进程的GPU

任务的顺序为PP第一，PME第二。默认情况下，具有不同类型GPU任务的进程的顺序是相同

的，但可以使用\-ddorder选项修改，并且在使用多个节点时可能变得相当复杂。注意，PP任务

的成键相互作用部分可以使用与短程相互作用部分相同的GPU运行，也可以在CPU上运行，通

过\-bonded选项进行控制。GPU任务分配（无论是手动设置还是自动）会在模拟所用的第一个

物理节点上的 mdrun ↪ 276 的输出中报告。例如：

gmx mdrun\-gputasks 0001 \- nb gpu\-pme gpu\-npme 1 \- ntmpi 4

会在日志文件/终端输出以下信息：

On host tcbl14 2 GPUs selected for this run\.

Mapping of GPU IDs to the 4 GPU tasks in the 4 ranks on this node:

PP: 0 ,PP: 0 ,PP: 0 ,PME: 1

在这种情况下，用户设置了 3 个进程在GPU 0上的进行PP计算工作， 1 个进程在GPU 1上进

行PME计算。GPU的详细索引也会输出到日志文件中。

有关GPU任务的更多信息，请参考 GPU 任务的类型↪ 88 。

\-pmefft 选择是在CPU上执行，还是在GPU上执行3D FFT计算。可以设置为 auto，cpu，gpu。

当PME转移到GPU上时，\-pmefft gpu为默认设置，整个PME计算都在GPU上执行。但

是，在某些情况下，例如，运行时使用了相对较慢或较老的GPU以及快速的CPU核心，通过在

CPU上计算FFT，将GPU的一些工作转移回CPU可以提高性能。

单节点 mdrun 的示例

gmx mdrun

使用所有可用的资源启动 mdrun ↪ 276 。 mdrun ↪ 276 会自动为线程MPI进程，OpenMP线程选择一个相当  
高效的划分，并将工作分配到兼容的GPU。具体细节会随硬件和运行的模拟类型而有所不同。

gmx mdrun\-nt 8

使用 8 个线程启动 mdrun ↪ 276 ，可能是线程MPI或OpenMP线程，具体取决于硬件和运行的模拟类型。

gmx mdrun\-ntmpi 2 \- ntomp 4

使用总共 8 个线程启动 mdrun ↪ 276 ，其中 2 个线程MPI进程，每个进程具有 4 个OpenMP线程。只有在  
寻求最佳性能时，你才应该使用这些选项，并且必须注意，你创建的进程可以将其所有的OpenMP线程  
都运行在同一插槽上。进程数应该是插槽数的倍数，每个节点的核心数应该是每个进程的线程数的倍数。

gmx mdrun\-ntmpi 4 \- nb gpu\-pme cpu

使用 4 个线程MPI进程启动 mdrun ↪ 276 。使用OpenMP线程将可用的CPU核心在进程之间平均分配。  
力的长程部分在CPU上计算。当硬件上的CPU与GPU相比性能相对强大时，这可能是最佳设置。成  
键部分力的计算会自动分配到GPU，因为力的长程部分是在CPU上计算的。

gmx mdrun\-ntmpi 1 \- nb gpu\-pme gpu\-bonded gpu\-update gpu

使用单个线程MPI进程启动 mdrun ↪ 276 ，会使用所有可用的CPU核心。所有可以在GPU上运行的相  
互作用类型都会这样做。当硬件上的CPU与GPU相比性能非常弱时，这可能是最佳设置。

gmx mdrun\-ntmpi 4 \- nb gpu\-pme cpu\-gputasks 0011

使用 4 个线程MPI进程启动 mdrun ↪ 276 ，并将它们映射到ID为 0 和 1 的GPU。使用OpenMP线程  
将可用的CPU核心在进程之间平均分配，前两个进程将短程非键力的计算转移到GPU 0，后两个进程  
则将其转移到GPU 1。力的长程部分在CPU上计算。当硬件上的CPU与GPU相比性能相对强大时，  
这可能是最佳设置。

gmx mdrun\-ntmpi 4 \- nb gpu\-pme gpu\-npme 1 \- gputasks 0001

使用 4 个线程MPI进程启动 mdrun ↪ 276 ，其中一个专门用于长程PME计算。前 3 个线程将其短程非键  
计算转移到ID为 0 的GPU，第 4 个（PME）线程将其计算转移到ID为 1 的GPU。

gmx mdrun\-ntmpi 4 \- nb gpu\-pme gpu\-npme 1 \- gputasks 0011

与上面的例子类似， 3 个进程被分配用于计算短程非键力，一个进程被分配用于计算长程力。在这种情  
况下， 3 个短程进程中的 2 个会将其非键力计算转移到GPU 0。ID为 1 的GPU计算第 3 个短程进程  
的短程力，以及PME专用进程的长程力。此示例或上面的示例的设置是否最佳取决于各个GPU的功  
能和系统组成。

gmx mdrun\-gpu\_id 12

使用ID为 1 和 2 的GPU启动 mdrun ↪ 276 （例如，因为GPU 0专门用于显示）。这需要两个线程MPI  
进程，并使用OpenMP线程在它们之间划分可用的CPU核心。

gmx mdrun\-nt 6 \- pin on\-pinoffset 0 \- pinstride 1  
gmx mdrun\-nt 6 \- pin on\-pinoffset 6 \- pinstride 1

启动 2 个 mdrun ↪ 276 进程，每个进程总共 6 个线程，通过分配给不重叠的物理核心，使进程间的相互影  
响尽可能小。线程会将其关联性设置到特定的逻辑核心，分别从第 1 个和第 7 个逻辑核心开始。上面的  
方法很适用于具有 6 个物理内核和启用超线程的Intel CPU。只有在限制 mdrun ↪ 276 使用一部分核心以  
便与其他进程共享节点时才使用这种设置。警告：对不同的操作系统，逻辑CPU/核心到物理核心的映  
射可能有所不同。在Linux上，可以使用cat /proc/cpuinfo来确定这个映射。

mpirun\-np 2 gmx\_mpi mdrun

当使用外部MPI编译的 gmx mdrun ↪ 276 时，这会启动两个进程，以及硬件和MPI设置所允许的尽可能  
多的OpenMP线程。如果MPI设置仅限于一个节点，那么 gmx mdrun ↪ 276 会局限于该节点。

#### 3\.15\.5 在多个节点上运行 mdrun

在多个节点上运行需要使用外部MPI库构建GROMACS。默认情况下，这样的 mdrun ↪ 276 可执行文件  
使用 gmx\_mpi mdrun运行。除 \-ntmpi和 \-nt会导致致命错误，需要通过MPI环境控制进程数外，  
运行单节点 mdrun ↪ 276 的所有注意事项仍然适用。使用多个节点时，诸如\-npme 之类的设置会更为重  
要。将MPI环境配置为在每个核上运行一个进程通常很好，直到接近强标度极限。到那时，需要使用  
OpenMP将MPI进程的工作分散到多个核心上，以便继续提高绝对性能。标度极限的位置取决于处理  
器，是否使用GPU，网络和模拟算法，但如果你需要最大吞吐量，可以试试~200粒子/核的设置。

在这些情况下，还有其他相关的命令行参数。

\-tunepme 默认为on，模拟\(2019版使用Verlet方案\)会优化PME和DD算法的各个方面，在进程

和/或GPU之间转移负载以最大限度地提高吞吐量。一些 mdrun ↪ 276 的功能与此不兼容，它们会

忽略此选项。

\-dlb 可以设置为 auto，no 或 yes。默认为 auto。为了最大限度地提高性能，需要在MPI进程

之间进行动态负载均衡。对于粒子或相互作用密度不均匀的分子体系，此选项尤为重要。当

性能损失超过某个阈值时，会激活DLB并在进程之间转移粒子以提高性能。如果可用，使用

\-bonded gpu有望提高DLB的能力，最大限度地提高性能。DLB与GPU驻留并行化（使用

sphinxupquote\-update gpu）不兼容，因此在此类模拟中仍处于关闭状态。

\-gcom 2019 版选项 在模拟过程中， gmx mdrun ↪ 276 必须在所有进程之间进行通信，以计算动能等量。默

认情况下，只要可行就会这样做，因此受很多 mdp 选项的影响。↪ 123 通信阶段之间的时间间隔必须

是 nstlist ↪ 128 的倍数，并且默认为 nstcalcenergy ↪ 128 和 nstlist ↪ 128 的最小值。mdrun \-gcom

设置这样的通信阶段之间必须经过的步数，当使用多个进程时，这可以提高性能。注意，这意味

着，例如温度耦合算法会有效地保持恒定的能量，直到下一个通信阶段。 gmx mdrun ↪ 276 会始终遵

照mdrun \-gcom的设置，如有必要，可以更改 nstcalcenergy ↪ 128 ， nstenergy ↪ 128 ， nstlog ↪ 127 ，

nsttcouple ↪ 137 和/或 nstpcouple ↪ 138 。

在模拟过程中，gmx mdrun必须在所有PP进程之间进行通信，以计算动能等物理量，用于日志文件报  
告，或者温度耦合。默认情况下，若设置了 mdp 选项,需要时就会这么做,这样通信阶段之间的周期就  
是 nstcalcenergy , nsttcouple ,和 nstpcouple 的最小公倍数\.

注意，在有多个节点的情况下，\-tunepme的作用更大，因为PP和PME进程的通信成本不同。这时  
仍然会在PP和PME进程之间转移负载，但不会改变正在使用的单独PME进程的数目。

还要注意，\-dlb和\-tunepme可能会相互干扰，因此如果遇到可能由此引起的性能变化，你可能需要  
单独调整PME，并使用mdrun \-notunepme \-dlb yes运行结果。

gmx tune\_pme ↪ 348 实用程序可用于搜索更广泛的参数空间，包括对 tpr ↪ 619 文件进行安全的更改，以及  
改变\-npme。它只知道MPI环境创建的进程数，并且在优化过程中不会明确地管理OpenMP的任何方  
面。

多节点 ____mdrun____ 的示例

单节点 mdrun ↪ 276 的示例和解释仍然相关，但不能再使用 \-ntmpi来选择MPI进程数。

mpirun\-np 16 gmx\_mpi mdrun

使用 16 个进程启动 gmx mdrun ↪ 276 ，由MPI库映射到硬件，例如，使用MPI主机文件中的指定。使用  
OpenMP线程将自动在进程之间划分可用的核，具体取决于硬件和环境设置，如OMP\_NUM\_THREADS。

mpirun\-np 16 gmx\_mpi mdrun\-npme 5

使用 16 个进程启动 gmx mdrun ↪ 276 ，如上所述，要求其中的 5 个进程专门用于PME计算。

mpirun\-np 11 gmx\_mpi mdrun\-ntomp 2 \- npme 6 \- ntomp\_pme 1

使用 11 个进程启动 gmx mdrun ↪ 276 ，如上所述，要求其中的 6 个进程专门用于PME计算，每个进程一  
个OpenMP线程。其余 5 个进程执行PP计算，每个进程使用 2 个OpenMP线程。

mpirun\-np 4 gmx\_mpi mdrun\-ntomp 6 \- nb gpu\-gputasks 00

在具有 2 个节点的机器上启动 gmx mdrun ↪ 276 ，总共使用 4 个进程，每个进程使用 6 个OpenMP线程，  
每个节点上的 2 个进程共享ID为 0 的GPU。

mpirun\-np 8 gmx\_mpi mdrun\-ntomp 3 \- gputasks 0000

使用与上面相同/类似的硬件，在具有 2 个节点的机器上启动 gmx mdrun ↪ 276 ，总共使用 8 个进程，每个  
进程使用 3 个OpenMP线程，每个节点上的 4 个进程共享ID为 0 的GPU。对于同样的硬件，这种设  
置可能会比前面的设置更快，也可能不会。

mpirun\-np 20 gmx\_mpi mdrun\-ntomp 4 \- gputasks 00

使用 20 个进程启动 gmx mdrun ↪ 276 ，将CPU核心均匀地分配给每个进程，每个进程一个OpenMP线  
程。如果有 10 个节点，每个节点有一个GPU，并且每个节点有 2 个插槽，每个插槽有 4 个核心，这种  
设置可能是合适的。

mpirun\-np 10 gmx\_mpi mdrun\-gpu\_id 1

使用 20 个进程启动 gmx mdrun ↪ 276 ，将CPU核心均匀地分配给每个进程，每个进程一个OpenMP线  
程。如果有 10 个节点，每个节点有 2 个GPU，但每个节点上的另一个作业使用GPU 0，这种设置可能  
是合适的。作业调度程序应该将两个作业的线程关联到为它们分配的核心，否则 mdrun ↪ 276 的性能会受  
到极大影响。

mpirun\-np 20 gmx\_mpi mdrun\-gpu\_id 01

使用 20 个进程启动 gmx mdrun ↪ 276 。如果有 10 个节点，每个节点有 2 个GPU，这种设置可能是合适  
的，但是对于节点上的所有GPU都可以使用的正常情况，无需指定 \-gpu\_id。

#### 3\.15\.6 接近标度极限 2019 版

当每个核的原子数接近当前的标度极限，~100个原子/核的时候，运行GROMACS模拟有几个方面非

常重要。

其中之一就是，在P\-LINCS中使用 constraints = all\-bonds会为区域的大小设置一个人为的最小  
值。你应该重新考虑对所有键都使用约束（并记住这么做对dt 的最大安全值可能产生的后果），或者  
适当地更改lincs\_order和lincs\_iter。

#### 3\.15\.7 避免对约束进行通信

由于执行一个MD步骤所需的时间非常短，特别是在接近标度极限时，任何通信都会因延迟开销和同步

而对性能产生负面影响。大部分通信是无法避免的，但有时可以完全避免约束坐标的通信。下面列出的

几点通常可以提高性能，在标度极限（约~100原子/核或~10000原子/GPU）时效果尤为显著。在进

行需要尽可能快的模拟,或强标度的基准测试时，应考虑到这些要点。

在可能的情况下，应该避免将P\-LINCS与constraints = all\-bonds一起使用。这不仅需要大量的通  
信，还会人为地设定分解域的最小尺寸。如果使用原子力场，并以2 fs的时间步长进行积分，通常可以  
换用constraints = h\-bonds约束,而不改变其他设置。实际上，大多数力场参数化时都使用了这些设  
置，因此这种做法更科学。

为了完全避免约束通信和/或在GPU上进行更新，体系需要支持所谓的”更新组”（或完全不存在约束）。  
当涉及耦合约束的所有原子都直接与一个中心原子耦合，连续有序，并且不被非约束原子分开时，体系  
就支持更新组。紧凑说明的甲基就是一个例子。对于使用constraints = h\-bonds的原子力场来说，这  
实际上意味着在拓扑中，氢原子与其相连的重原子相邻。此外，当存在虚拟位点时，构造原子应全部约  
束在一起，虚拟位点和构造原子应连续，但顺序并不重要。TIP4P水模型就是这样的一个例子。日志文  
件中会注明是否使用了更新组。如果不能使用，也会注明原因。

#### 3\.15\.8 如何更好地运行 mdrun

Wallcycle模块用于测量 gmx mdrun ↪ 276 的运行时性能。在每个运行的日志文件的末尾，Real cycle and  
time accounting 部分会提供一个表，表格行中包含了 gmx mdrun ↪ 276 代码不同部分的运行时统计信  
息。该表的列给出了运行相应部分所用的进程数和线程数，整个运行期间统计的（所有线程和进程）平  
均的墙钟时间和周期计数。最后一列还显示了每行所代表的总运行时间的百分比。注意， gmx mdrun ↪ 276  
定时器重置功能（\-resethway 和\-resetstep）会重置性能计数器，因此有助于避免运行开始时的启  
动开销和性能不稳定（例如，由于负载均衡导致）。

性能影响因素包括：

- 粒子网格Ewald过程中的粒子\-粒子计算
- 区域分解
- 区域分解通信负载
- 区域分解通信范围
- 虚拟位点约束
- 将坐标X发送到粒子网格Ewald
- 邻区搜索
- 启动GPU操作
- 坐标通信
- 力
-  等待\+力的通信
- 粒子网格Ewald
- PME重新分布坐标X/力F
- PME传播
- PME收集
- PME 3D\-FFT
- PME 3D\-FFT通信
- PME处理Lennard\-Jones
- PME处理静电
- PME等待粒子\-粒子
- 等待\+接收PME力
- 等待GPU非局部
- 等待GPU局部
- 等待PME GPU传播
- 等待PME GPU收集
- 归约PME GPU力
- 非键位置/力缓冲区操作
- 虚拟位点传播
- 质心牵引力
- AWH（加速权重直方图法）
- 输出轨迹
- 更新
- 约束
- 能量的通信
- 强制旋转
- 添加旋转力
- 位置交换
- 交互MD
- MD图

由于每次运行都会收集性能数据，这些数据对于评估和调整 gmx mdrun ↪ 276 的性能至关重要。因此，它  
们既有利于代码开发人员，也有利于程序用户。计数器是模拟的不同部分所耗时间/周期的平均值，因此

##### 不能直接给出单次运行期间的波动（尽管多次运行的比较仍然非常有用）。

只有当代码的相关部分在 gmx mdrun ↪ 276 运行期间被执行时，计数器才会出现在MD日志文件中。还有  
一个名为Rest的特殊计数器，用于指示上述任何计数器未计入的时间。因此，大量的Rest时间（超  
过百分之几）通常表示并行化效率低下（例如，串行代码），建议将其报告给开发人员。

另外一组子计数器可以提供更细粒度的性能检查。它们是：

- 区域分解重新分布
- DD邻区搜索格点\+排序
- DD设置通信
- DD生成拓扑
- DD生成约束
- DD处理拓扑其他
- 邻区搜索格点局部
- NS格点非局部
- NS搜索局部
- NS搜索非局部
- 成键力
- 成键FEP力
- 限制力
- 列出的缓冲区操作
- 非键修剪
- 非键力
- 启动非键GPU任务
- 启动PME GPU任务
- Ewald力修正
- 非键位置缓冲区操作
- 非键力缓冲区操作

子计数器是面向开发人员的，必须在编译期间启用。更多信息，请参阅/dev\-manual/build\-system。

#### 3\.15\.9 使用 GPU 运行 mdrun

##### GPU 任务类型

为更好地理解后面关于GPU计算短程, PME ,成键相互作用以及更新和约束的不同使用案例，我们先

介绍下不同GPU任务的概念。在考虑运行模拟时，必须计算原子之间的几种不同类型的相互作用（更

多信息见参考手册↪ 469 ）。因此，计算可以划分成几个不同的部分，这些部分在很大程度上彼此独立（因

此可以按任何顺序计算，例如，按顺序计算或同时计算），在时间步结束时会将这些计算的信息组合起来，

获得每个原子上最终的力，并将系统演化到下一个时间点。为更好地理解请参阅以下章节区域分解↪ 76 。

对MD步骤所需的所有计算，GROMACS会从最低级别（SIMD单元，核心，插槽，加速器等）自下

而上地优化每个步骤的的性能。因此，许多单独的计算单元都针对最低级别的硬件并行性进行了高度调

整：SIMD单元。此外，使用GPU加速器作为协处理器时，可以转移一些工作，也就是，使用加速器

设备上的CPU同时/并发计算，并将结果通信给CPU。目前，GROMACS支持GPU加速器转移两项

任务，短程的实空间中的非键相互作用↪ 88 ，以及 PME ↪ 89 。

GROMACS支持两种主要的卸载模式：力卸载和GPU驻留。前者涉及卸载部分或全部相互作用计算，

并在CPU上进行积分（因此要求每步数据移动）。而在GPU驻留模式中，通过卸载积分和约束（如果

用到），所需的数据移动次数较少。

力卸载模式是更广泛支持的GPU加速模式，在各种GPU加速器（NVIDIA、AMD和Intel）上都支  
持短程非键卸载。这与绝大多数功能和并行化模式兼容，并可用于扩展到大型机器。将短程非键和长程  
PME工作都卸载到GPU加速器上在功能和并行化兼容性方面有一些限制（请参阅下文）。CUDA和  
SYCL支持卸载（大多数类型的）成键相互作用。CUDA和SYCL支持GPU驻留模式，但有额外的限  
制，详见 GPU 更新\.。

2019 :注意，在 ____GPU____ 上求解 ____PME____ 仍然只是初始版本，具有下面会进一步概述的一系列限制。

目前，我们一般支持在各种GPU加速器（包括NVIDIA和AMD）上对使用动态修剪和不使用动态修  
剪的短程非键计算进行转移。这与绝大多数功能和并行化模式兼容，并可用于扩展到大型机器。

同时将短程非键和长程PME工作转移到GPU加速器是一项新功能，在功能和并行兼容性方面存在一  
些限制（请参阅下面的章节↪ 89 ）。

##### 短程非键相互作用的 GPU 计算

与只使用CPU运行相比，将GPU用于短程非键相互作用计算所得的性能提升占据了可能提升的大部

分。这种情况下，GPU充当加速器，可以有效地并行化这个问题，从而减少计算时间。

PME 的 GPU 加速计算

GROMACS可以将PME计算转移到GPU，以进一步减少CPU负载并改善CPU和GPU之间的使用

重叠。这种情况下，在相同GPU上除了计算短程相互作用之外，还会求解PME。

已知限制

请再次注意下面列出的限制\!

- 2019: PME的GPU卸载功能可以在使用CUDA的NVIDIA硬件或使用OpenCL的AMD硬件  
上使用。
- GPU上只支持阶数为 4 的PME。
- 2019:只有当一个进程仅有一个PME任务时，PME才可以在GPU上运行，即，不支持使用多个  
进程进行PME分解。
- 2019:只支持单精度。
- 2019:不支持电荷微扰的自由能计算，因为只能计算单个PME格点。
- 只支持动力学积分方法（即，跳蛙式，速度Verlet，随机动力学）
- GPU不支持LJ PME。
- 当使用针对AMD/NVIDIA GPU的oneAPI,以SYCL构建GROMACS时，仅支持混合模式  
（\-pmefft cpu）。如果使用针对Intel GPU的oneAPI,针对AMD/NVIDIA GPU的hipSYCL，  
则支持完全卸载PME。

##### GPU 加速的成键相互作用计算（ CUDA 和 SYCL ）

GROMACS可以将PP工作负载的成键部分转移到兼容的GPU上。它被当作PP工作的一部分，并要

求短程非键任务也在GPU上运行。通常情况下，卸载成键相互作用具有性能优势，尤其是当每个GPU

的CPU资源相对较少时（可能是因为CPU性能较弱，或者在运行中分配给GPU的CPU内核较少），

或者当CPU上还有其他计算时。后者的一个典型例子就是自由能计算。

2019:通常只有当CPU与GPU相比相对较弱时，这种做才有优势，可能是因为其工作负载对于可用的

核来说太大。自由能计算可能就是这种情况。

约束计算和坐标更新的 GPU 加速 \( 仅限 CUDA 和 SYCL\)

GROMACS还可以在GPU上执行坐标更新以及（需要的）约束计算。这种并行模式称为”GPU驻留”，

因为所有力和坐标数据都可以在GPU上保留若干步（通常是在温度/压力耦合或邻区搜索步骤之间）。

GPU驻留模式允许在GPU上执行模拟步骤的所有（支持的）计算。这样做的好处是减少了CPU主机

和GPU之间的耦合，在典型的MD步骤中，数据无需在CPU和GPU之间传输，而力卸载方案则要

求每一步都在CPU和GPU之间传输坐标和力。不过，GPU驻留方案仍能在GPU计算的同时在CPU

上进行部分计算。这有助于支持GROMACS的各种功能，因为并非所有功能都能移植到GPU上。与

此同时，它还能通过利用否则会大部分闲置的CPU来提高性能。将成键或PME计算移回CPU通常是

有利的，但具体细节取决于一个模拟中CPU内核与GPU配对时的相对性能。

默认启用GPU驻留模式（如果支持的话），当构建配置或模拟设置与之不兼容时，会自动回退到CPU

更新模式。可以通过设置GMX\_FORCE\_UPDATE\_DEFAULT\_CPU环境变量来更改默认行为。在这种情况下，

遵循默认行为（即\-update auto）的模拟会在CPU上运行更新。

在快速GPU与较慢CPU配合使用的情况下，使用这种并行模式通常具有优势，尤其是在GPU上只分  
配了单个模拟的情况下。然而，在典型吞吐量的情况下，每个GPU都会分配多个运行，卸载所有工作，  
尤其是不将部分工作移回CPU的情况下，其性能会比只卸载力计算的并行模式更差。

将任务分配给 GPU

根据应在哪些硬件上执行哪些任务，可以在相同或不同的GPU上组合不同类型的计算，这取决

于 mdrun ↪ 276 运行时提供的信息。

可以将不同计算任务的计算分配给相同的GPU，这意味着它们将共享同一设备上的计算资源，或者分  
配到不同处理单元，每个处理单元执行一个任务。

下面概述了可能的任务分配：

GROMACS 2018版：

可使用两种不同类型的可分配GPU加速的任务：\(短程\)非键和PME。每个PP进程都有

一个非键任务，可以转移到GPU。如果只有一个具有一个PME任务的进程（包括该进程是

单纯的PME进程），那么该任务可以转移到GPU。这样的PME任务可以完全在GPU上

运行，或者可以只在CPU上运行它的后几个阶段。

##### 限制是GPU上的PME不支持PME区域分解，因此只能将一个PME任务转移到分配给

##### 单独PME进程的单个GPU上，而非键可以分解并转移到多个GPU上。

##### GROMACS 2019版：

##### 没有新的可分配的GPU任务可用，但任何成键相互作用的计算工作所在的GPU可以与PP

任务所用的短程相互作用GPU相同。这可以通过\-bonded选项来更改。

GROMACS 2020版:

更新和约束可以在同一GPU上运行,就像PP任务中的短程非键和成键相互作用那样。这可

能受\-update标识影响。

GROMACS 2021/2022版:

在CUDA构建中通信和辅助任务也可以卸载。在区域分解环交换和PP\-PME通信中，GPU

之间的传输不再通过CPU分次进行，而是可以直接进行GPU\-GPU通信。作为环交换的一

项辅助任务，数据打包和解包的工作也卸载到GPU上。在 2021 版中，使用线程\-MPI实现

这一功能，而从 2022 版开始，也可以使用GPU感知MPI实现这一功能。直接GPU通信

默认情况下并未启用，可以使用GMX\_ENABLE\_DIRECT\_GPU\_COMM环境变量启用（仅对支持

的系统有效）。

GROMACS 2023版:

更新默认在支持模拟设置的GPU上运行；注意，这仅适用于CUDA和SYCL，不适用于

OpenCL。

PME分解支持增加了额外的与并行相关的辅助GPU任务，包括网格打包和归约操作,以及

分布式GPU FFT计算。

新增了对CUDA图形调度的试验性支持，支持大多数不需要CPU力计算的GPU驻留运行。

##### GPU 任务的性能注意事项

##### 1\)性能均衡取决于所用CPU核心的速度和数目，所用GPU的速度和数目。

##### 2\)与力卸载模式相比，GPU驻留并行模式（卸载更新/约束）对适当的CPU\-GPU平衡不太敏感。

##### 3\)如果机器具有许多慢/旧的GPU，和/或多核的快速/现代CPU，让CPU进行PME计算，GPU

##### 只进行非键计算可能更好。

##### 4\)如果机器有快速/现代的GPU，和/或少量核的慢/旧CPU，GPU执行PME通常更好。

##### 5\)将成键计算卸载到GPU通常不会提高模拟性能，因为基于CPU的高效内核可以在GPU完成其

他卸载工作之前完成成键计算。因此，当卸载PME时，gmx mdrun默认会卸载非键计算。通过

成键卸载可以提高性能的典型情况是：具有大量的成键计算工作（例如，纯脂质或溶剂很少大部

分是聚合物的系统），每个GPU的CPU核心很少和/或很慢，或者当CPU进行其他计算（例如

PME，自由能）。

6\)2019:有可能使用多个可以转移PME的GPU，例如， 3 个MPI进程每个使用一个GPU计算短

程相互作用，而第 4 个进程使用其GPU计算PME。

7\)在大多数现代硬件上，GPU驻留模式（默认）比力卸载模式更快，尽管它可能会使得CPU闲置。

将成键工作移回CPU（\-bonded cpu）,比起将积分和约束放在CPU上是利用快速CPU的更好

方法。唯一的例外可能是多重模拟,这种情况先每个GPU都分配了大量模拟。

##### 8\)在大多数情况下，GPU直接通信会优于分阶段通信（线程MPI和MPI都是这样）。理想情况下，

##### 它应与GPU驻留模式相结合，以达到最佳性能。

##### 9\)要确定哪种方案最适合你的机器，唯一的方法就是测试和检查性能。

##### 减少 GPU 加速运行中的开销

##### 为了使CPU核和GPU协同执行，任务是在GPU上异步启动和执行的，而CPU核执行非转移力的计

##### 算（如计算成键力或自由能计算,对 2019 版则为长程PME静电）。异步任务启动由GPU设备驱动程

##### 序处理，需要CPU的参与。因此，调度GPU任务需要CPU资源，这些资源可能会与其他CPU任务

##### 竞争，造成干扰，从而导致速度减慢。

##### 因此，调度GPU任务的工作会产生开销，在某些情况下可能会显著延迟或干扰CPU的执行。

CPU执行的延迟是由启动GPU任务的延迟引起的，随模拟ns/day的增加，开销可能会变得很大（即每  
步的墙钟时间更短）。 gmx mdrun ↪ 276 会测量启动GPU工作的开销，并将其输出到日志文件的性能摘要  
部分（Launch PP GPU ops\./Launch PME GPU ops\.列）。运行时间有百分之几消耗在启动工作是正常  
的，但在快速迭代和多GPU并行运行中，可能会有10%或更大的开销。这是否会对性能产生重大影响，  
取决于MD主步骤中的工作有多少分配给了CPU。在大部分或全部力计算被卸载的情况下，当CPU不  
参与通信时（例如启用线程MPI和GPU直接通信），大的启动成本可能不会导致大的性能损失。然而，  
当CPU分配了计算任务（例如在自由能或牵引/AWH模拟中）或从CPU启动MPI通信（即使使用  
GPU感知MPI）时，GPU启动成本将与其他CPU工作相竞争，从而产生开销。通常，用户几乎无法  
避免此类开销，但在一些情况下，进行调整可以提高性能。在OpenCL运行中，默认情况下会启用GPU  
任务计时，虽然在大多数情况下其影响很小，但在快速运行中性能可能会受到影响。\(2019:对于使用  
CUDA的NVIDIA GPU，性能影响最大，而对于使用OpenCL的AMD和Intel则影响更小。\)在这些  
情况下，如果观察到超过百分之几的Launch GPU ops时间，建议通过设置GMX\_DISABLE\_GPU\_TIMING  
环境变量来关闭计时。在多个进程共享一个GPU的并行运行中，也可以通过减少每个GPU启动的线  
程MPI或MPI进程来减少启动开销；例如，每个线程或核心一个进程常常不是最佳的。CUDA图功  
能（GROMACS 2023中添加）的目标是减少此类开销并提高GPU工作调度效率，因此它可以显著改  
善，特别是对于在快速GPU上运行的小型模拟体系。由于这是一项新功能，在 2023 版本中，需要使用  
GMX\_CUDA\_GRAPH环境变量来启用对CUDA图的支持。

第二类开销，即GPU运行时或驱动程序对CPU计算的干扰，是由GPU任务的调度和协调引起的。  
单独的GPU运行时/驱动程序线程可能需要CPU资源，这可能会与并发运行的非卸载任务发生竞争，  
从而可能降低CPU工作\(PME或成键力计算\)的性能。\(2019:当使用带有OpenCL的AMD GPU，  
且驱动程序版本较旧（例如fglrx 12\.15）时，这种效果最为明显。\)为最大限度地减少开销，建议在  
启动 gmx mdrun ↪ 276 时不要使用CPU硬件线程，特别是在具有高核心计数和/或启用了同时多线程的  
CPU上。例如，在具有 16 核CPU， 32 个线程的机器上，试试gmx mdrun \-ntomp 31 \-pin on。这  
会为GPU任务调度留出一些CPU资源，可能会减少对CPU计算的干扰。注意，将更少的资源分配  
给 gmx mdrun ↪ 276 CPU计算时需要权衡，对于每个GPU有多个CPU核心,可能不太显著,但在某些情  
况下（例如使用多进程MPI运行），这可能会导致复杂的资源分配，并可能超过减少GPU调度开销所  
带来的好处,因此,我们建议在采用这些技术之前，先测试替代方案。

#### 3\.15\.10 运行 OpenCL 版本的 mdrun

##### 目前支持的硬件架构是：

##### • 基于GCN,基于CDNA的AMD GPU;

- Volta之前的NVIDIA GPU;
- Intel iGPU。

请确保安装了最新的驱动程序。对于AMD GPU，建议使用面向计算的 ROCm↪https://rocm\.github\.io/堆栈；  
或者，也兼容AMDGPU\-PRO堆栈；不建议使用过时且不受支持的fglrx专有驱动程序和运行时（但对  
于某些较旧的硬件，这可能是唯一支持的方法）。此外，还支持使用LLVM 4\.0或更高版本的Mesa 17\.0或  
更高版本。对于NVIDIA GPU，需要使用专有驱动程序，因为开源nouveau驱动程序（Mesa中提供）不  
支持OpenCL。对于Intel的集成GPU，建议使用 Neo驱动程序↪https://github\.com/intel/compute\-runtime/releases。  
更多Intel驱动程序的建议有待将来增加。所需的最小OpenCL版本为1\.2。另见已知限制↪ 93 。

AMD GCN架构（所有系列）的设备兼容并会定期测试；已知NVIDIA Kepler及更高版本（计算能力  
3\.0）可以正常工作，但在进行成品运行之前，请务必确保GROMACS测试在硬件上成功通过。

OpenCL GPU内核是在运行时编译的。因此，构建OpenCL程序可能需要几秒钟的时间，这会在 gmx  
mdrun ↪ 276 启动过程中引入轻微的延迟。对于长时间的成品MD这通常不是问题，但你可能希望改进这  
个问题，例如首先只使用CPU运行很少几步（例如，见上文\-nb选项）。

用于选择CUDA设备或用于定义GPU到PP进程映射的\-gpu\_id选项（或GMX\_GPU\_ID 环境变量）  
同样可以用于OpenCL设备。

开发人员可能会对其他一些 OpenCL 管理↪ 68 环境变量感兴趣。

____OpenCL____ 支持的已知限制

下面是当前OpenCL支持的一些限制，GROMACS用户可能会感兴趣：

- 支持Intel集成GPU。不支持Intel CPU和Xeon Phi。当编译GROMACS以便在消费级Intel GPU  
（而非Ponte Vecio / Data Center Max GPU）上运行时，请设置\-DGMX\_GPU\_NB\_CLUSTER\_SIZE=4  
。
- 由于NVIDIA OpenCL运行时中某些异步任务排队函数的阻塞行为，如果使用受影响的驱动程序  
版本，那么使用NVIDIA GPU时几乎没有性能提升。此问题会影响直到 349 系列的NVIDIA驱  
动程序版本，但已经修复了 352 及更高版本的驱动程序。
- 在NVIDIA GPU上，由于NVIDIA OpenCL编译器的限制，OpenCL内核的性能远低于同等的  
CUDA内核。
- 在NVIDIA Volta和图灵架构上，OpenCL代码在驱动程序版本高达440\.x时仍会产生不正确的结  
果（很可能是由于编译器问题）。在这些架构上运行通常会失败。
- 2019: PME目前仅在AMD设备上受支持，因为其他供应商的设备存在已知问题。

GROMACS开发人员感兴趣的限制\(2019\)：

- 对于未使用warp/wavefronts或warp/wavefront大小不是 32 的倍数的OpenCL设备，当前实现  
不兼容

#### 3\.15\.11 运行 SYCL 版本的 mdrun

##### 确保安装了最新的驱动程序，并查看安装指南，了解兼容硬件和软件的列表以及编译时推荐的选项。

##### 请记住以下可能有用的环境变量：

- 使用oneAPI运行时:  
____\-____ SYCL\_CACHE\_PERSISTENT=1:启用GPU核心缓存,减少gmx mdrun启动时间\.

除\-gpu\_id选项外,特定后端的环境变量,如 SYCL\_DEVICE\_FILTER或ROCR\_VISIBLE\_DEVICES,可用  
于选择GPU\.

#### 3\.15\.12 性能检查清单

##### 有许多不同方面的因素会影响GROMACS模拟的性能。大多数模拟需要大量的计算资源，因此优化这

##### 些资源的使用是值得的。下面的清单中提到的几个问题可能导致 2 倍的性能差异。因此，检查下清单可

##### 能很有用。

##### GROMACS 配置

##### • 除非绝对确定，否则不要使用双精度。

- （自己）编译FFTW库时要使用x86上的正确选项（在大多数情况下，会自动配置正确的选项）。
- 在x86上，使用gcc作为编译器（不要使用icc, pgi或Cray编译器）。
- 在POWER上，使用gcc而不是IBM的xlc。
- 使用新的编译器版本，尤其是gcc（例如，从版本 5 到 6 ，编译后的代码性能有了很大的提高）。
- MPI库：OpenMPI通常性能良好，并且几乎没有问题。
- 确保你的编译器支持OpenMP（某些版本的Clang不支持）。
- 如果你的GPU支持CUDA, OpenCL或SYCL，请使用它们。  
____\-____ 配置时指定\-DGMX\_GPU=CUDA,\-DGMX\_GPU=OpenCL,或\-DGMX\_GPU=SYCL。  
____\-____ 对于CUDA，请使用与GPU匹配的最新CUDA，以利用最新的性能增强功能。  
____\-____ 使用最新的GPU驱动程序。  
____\-____ 确保 gmx mdrun ↪ 276 使用的GMX\_SIMD与CPU架构匹配；如果使用的设置并不是最佳的，日  
志文件会给出警告说明。但是，在GPU或高度并行的MPI运行中，AVX2优于AVX512（更  
多信息参见核内并行化↪ 76 ）。  
____\-____ 如果在集群的登录节点上编译，请确保计算节点支持GMX\_SIMD。

##### 运行设置

##### • 对于近似球形的溶质，使用菱形十二面体单位晶胞。

- 如 果 使 用 的 时 间 步 长 <=2\.5 fs， 使 用 constraints=h\-bonds ↪ 140 （而 不 使  
用 constraints=all\-bonds ↪ 140 ），因为  
____\-____ 这样速度更快，特别是使用GPU时;  
____\-____ 有必要能够使用GPU驻留模式；  
____\-____ 而且大多数力场在参数化时只约束涉及氢的键。
- 使用虚拟位点（gmx pdb2gmx \-vsite h）时，可以将时间步长增加到 4 或5 fs。
- 对于使用PME的大规模并行运行，你可能需要测试不同数目的PME进程（gmx mdrun \-npme  
???）以获得最佳性能； gmx tune\_pme ↪ 348 可以自动进行这种搜索。
- 对于大规模并行运行（也包括gmx mdrun \-multidir），或者网络速度较慢时，全局通信可能成  
为瓶颈，你可以为像温度和压力耦合这样的算法选用大的周期来减少影响\.  
2019:使用gmx mdrun \-gcom 来减少全局通信（请注意，此选项确实会影响温度和压力耦合的频  
率）。

##### 检查并改进性能

- 查看md\.log文件的末尾，查看MD计算的不同部分的性能，周期计数器以及墙钟时间。程序还  
会输出PP/PME负载比，并在因负载不均衡而导致大量性能损失时给出警告。
- 当PP/PME非均衡性很大时，调整PME进程的数目和/或截断以及PME格点的间距。注意，即  
使报告的非均衡性很小，自动化的PME调整也可能减少了初始的非均衡性。你仍然可以通过更改  
mdp参数或增加PME进程数来获得性能提升。
- \(特别是\)对于GPU驻留模式的运行\(\-update gpu\):  
____\-____ 频繁的维里或能量计算会产生很大的开销（这不会显示在循环计数器中）。为了减少这种开  
销，请增加nstcalcenergy；  
____\-____ 频繁的温度或压力耦合会产生巨大的开销；为减少这种情况，请确保在算法允许的范围内尽  
量减少耦合频率（通常为>=50\-100步）。
- 如果邻区搜索和/或区域分解需要花费大量时间，请增加nstlist如果使用了Verlet缓冲容差,  
gmx mdrun会自动增加此值,并且会增加成对列表缓冲以保持能量漂移不变。  
____\-____ 特别是使用多GPU运行时，在启动时自动增加nstlist可能会比较保守，较大的值往往是  
最佳值（例如，在使用PME和默认Verlet缓冲区容差的情况下，nstlist=200\-300）。  
____\-____ 在使用CUDA图时，对nstlist的值应避免使用奇数，以尽量减少与图实例化相关的开销。
- 如果Comm\. energies需要花费很多时间（会在日志文件中给出信息），增加nstcalcenergy或  
2019 版使用mdrun \-gcom。
- 如果所有通信都需要花费大量时间，你可能使用的核过多，或者你可以试试组合MPI/OpenMP并  
行，每个MPI进程运行 2 个或 4 个OpenMP线程。
- 在多GPU运行中，避免进程数目与内核（或硬件线程）一样多，由于多个MPI进程共享GPU  
产生的开销，从而导致效率大大降低。每个GPU最多使用几个进程，1\-3个进程通常是最佳选择；

##### 在GPU驻留模式和直接GPU通信中， 1 进程/GPU通常是最佳选择。

## 第 4 章

### 操作指南

这里提供了一些简短的操作指南，帮助用户开始进行模拟。Justin Lemkul提供了一些有用的 第三方教  
程↪http://www\.mdtutorials\.com/。

### 4\.1 初学者

##### 对于刚开始接触的人而言，GROMACS和/或分子动力学模拟↪ 62 可能非常复杂，令人生畏。强烈建议你

##### 先阅读GROMACS提供的各种文档，以及自己感兴趣的领域中相关的论文。

#### 4\.1\.1 资源

##### • GROMACS参考手册↪ 469 \- 非常详细的文档，也可以作为一份非常好的 MD ↪ 62 一般概念的介绍。

##### • 流程图↪ 32 \- 典型GROMACS MD过程的简单流程图，模拟水盒子中的蛋白质。

- 分子动力学模拟和GROMACS介绍（幻灯片↪https://extras\.csc\.fi/chem/courses/gmx2007/Berk\_talks/forcef\.pdf，视  
频↪https://video\.csc\.fi/playlist/dedicated/0\_7z3nas0q/0\_9aehv6v2）\-力场，积分器，温度和压力的控制（Berk Hess）。

### 4\.2 向力场中添加残基

#### 4\.2\.1 添加新残基

如果需要向现有的力场中引入新的残基，以便可以使用 pdb2gmx ↪ 297 进行处理，或者需要修改现有的残  
基，那么需要修改几个文件。有关所需格式的说明，你必须阅读参考手册↪ 469 ，并遵循以下步骤：

1\.将残基添加到所选力场的 rtp ↪ 615 文件中。你可以复制现有残基，对其进行重命名并适当修改，或

者你可以使用外部拓扑生成工具并将结果调整为 rtp ↪ 615 格式。

2\.如果你需要自动为残基添加氢原子，那么还需要在相关的 hdb ↪ 611 文件中创建一个条目。

97

3\.如果要引入新的原子类型，需要将它们添加到atomtypes\.atp和ffnonbonded\.itp文件中。

4\.如果需要任何新的成键类型，需要将它们添加到ffbonded\.itp文件中。

5\.将残基添加到residuetypes\.dat文件中，并指定适当的类别（蛋白质，DNA，离子等）。

6\.如果残基涉及与其他残基的特殊连接，需要更新specbond\.dat。

注意，如果你要做的只是模拟水溶液中的一些新奇配体，或者与常规蛋白质结合的一些新奇配体，那么  
可以生成单独的一个包含 \[ moleculetype \]的 itp ↪ 611 文件（例如，通过修改某些参数化服务器生成  
的 top ↪ 617 文件），并使用\#include将 itp ↪ 611 文件插入到不含该配体的系统的 top ↪ 617 文件中，这种作法  
比上面的做法更简单。

#### 4\.2\.2 修改力场

修改力场时，最好将已安装的力场目录的完整副本和residuetypes\.dat文件复制到本地工作目录中：

cp \-r $GMXLIB/residuetypes\.dat $GMXLIB/amber99sb\.ff\.

然后，像上面那样修改这些本地副本。 pdb2gmx ↪ 297 会同时找到原始版本和修改版本，你可以从给出的列  
表中交互地选择修改版本，或者你可以为 pdb2gmx ↪ 297 指定\-ff选项，这样本地版本就会覆盖系统版本。

### 4\.3 水溶剂化

当使用 solvate ↪ 328 生成溶剂盒子时，你需要为它提供一个预平衡好的合适的溶剂盒子，这样 solvate ↪ 328 可  
以将其堆积在溶质周围，然后再进行截取以得到你需要的模拟盒子大小。使用任何三位点水模型时（例  
如SPC，SPC/E或TIP3P）都可以指定\-cs spc216\.gro，此文件位于gromacs/share/top目录。你  
也可以使用其他水模型（例如TIP4P和TIP5P）。检查GROMACS安装目录下/share/top子目录的  
内容。溶剂化后，确保在所需温度下至少平衡5\-10 ps。你需要在 top ↪ 617 文件中选择正确的水模型，可  
以使用 pdb2gmx ↪ 297 的\-water 选项来指定所需的水模型，也可以手动编辑 top ↪ 617 文件来添加所需的水  
模型。

关于如何使用除水以外的溶剂，请参阅非水溶剂化↪ 99 或混合溶剂↪ 99 。

### 4\.4 将 3 位点水模型更改为 4 位点水模型

如果你有一个 3 位点水模型的\.gro文件，想要在保留水坐标的同时将其更改为 4 位点水模型，只要在  
每个水分子后面添加一个虚拟位点即可。假定三位点水模型中的原子名称依次为OW，HW1，HW2，文件  
为a\.gro，可以按照以下步骤进行操作：

1\.cat a\.gro | awk '\{print $0; if\($2=="HW2"\) printf\("%8s MW %4d%8\.3f%8\.3f%8\.3f\\␣

↪n",$1,$3,$4,$5,$6\)\}' > b\.gro

2\.修改b\.gro文件第二行中的原子数

3\.editconf \-f b\.gro \-o c\.gro  
4\.使用c\.gro进行短时间的能量最小化

### 4\.5 非水溶剂

##### 在GROMACS中可以使用水以外的溶剂。唯一的要求是，你需要一个预平衡好的盒子，其中包含你需

要的任何溶剂，以及模拟该物种的合适参数。然后就可以使用 solvate ↪ 328 的\-cs选项指定溶剂盒子进行  
溶剂化。

你可以在 virtualchemistry↪https://virtualchemistry\.org/ 找到一系列约 150 种不同的平衡好的液体，它们经过  
验证，可用于GROMACS，并可以使用OPLS/AA力场和GAFF力场。

#### 4\.5\.1 制作非水溶剂盒子

选择盒子密度和盒子大小。大小不一定是最终模拟盒子的大小\-一个边长1 nm的立方体盒子可能就好  
了。生成单个溶剂分子。计算出单个分子在所选密度和大小的盒子中会占据多少体积。使用 editconf ↪ 231  
在单个分子周围放一个所需大小的盒子。然后使用 editconf ↪ 231 将分子移动到稍微偏离中心的位置。然后  
使用 genconf ↪ 247 \-rot 将该盒子复制到大小和密度正确的一个大盒子中。然后使用NVT和周期性边界  
条件进行彻底平衡，以消除分子残存的有序性。现在你有了一个盒子，可以用于 solvate ↪ 328 的\-cs选项，  
这样会复制这个盒子以使其适应实际模拟盒子的大小。

### 4\.6 混合溶剂

##### 新用户面临的一个常见问题是，如何创建混合溶剂系统（例如，具有给定浓度的尿素或二甲基亚砜水溶

##### 液）。达到此目的的最简单步骤如下：

##### • 根据系统的盒子大小，确定所需的共溶剂分子的数目。

- 生成共溶剂单个分子的坐标文件（即urea\.gro）。
- 使用 gmx insert\-molecules ↪ 264 的\-ci \-nmol选项将所需数目的共溶剂分子添加到盒子中。
- 借助 gmx solvate ↪ 328 或 gmx insert\-molecules ↪ 264 程序，用水（或任何其他溶剂）填充盒子的其余部  
分。
- 编辑拓扑↪ 617 文件，\#include相应的 itp ↪ 611 文件，并修改\[ molecules \]指令以包含系统中的  
所有的物种。

### 4\.7 添加二硫键

最简单的方法是使用specbond\.dat文件和 pdb2gmx ↪ 297 实现的机制。你可能会发现 pdb2gmx ↪ 297 \-ss yes  
很有用。硫原子需要与 pdb2gmx ↪ 297 转换后的moleculetype处于相同的单元中，因此调用 pdb2gmx ↪ 297  
时，可能需要指定正确的\-chainsep选项。参见 pdb2gmx ↪ 297 \-h。这就要求，两个硫原子处于距离\+容  
差（通常为10%）范围内，才能被识别为二硫键。如果两个硫原子的距离没有近，那么你可以：

- 编辑specbond\.dat文件，允许形成二硫键，非常小心地进行能量最小化使键弛豫到合理的长度，  
或者
- 在这些硫原子之间使用大的力常数施加距离限制（但没有二硫键），运行初步的EM或MD，使它  
们的距离接近现有的specbond\.dat中的范围，以便为第二次调用 pdb2gmx ↪ 297 提供合适的坐标文  
件。

否则，手动编辑 top ↪ 617 文件是唯一可行的方法。

### 4\.8 在 GROMACS 中运行膜模拟

#### 4\.8\.1 运行膜模拟

##### 用户在模拟脂质双层时经常会遇到问题，特别是涉及蛋白质时。想要模拟膜蛋白的用户可以参考这个

教程↪http://www\.mdtutorials\.com/gmx/membrane\_protein/index\.html。

模拟膜蛋白的一种方案包括以下步骤：

1\.选择包含蛋白质和脂质参数的力场。

2\.将蛋白质插入膜中。（例如，使用g\_membed将蛋白嵌入预先构建好的双层上，或者进行粗粒化自

组装模拟再转换回全原子表示。）

3\.溶剂化系统，添加离子中和过量电荷并调整最终的离子浓度。

4\.能量最小化。

5\.让膜适应蛋白质。对所有蛋白质的重原子施加限制（1000 kJ/\(mol nm^2\)），通常运行约5\-10 ns

MD。

6\.去除限制，进行平衡。

7\.运行成品MD。

#### 4\.8\.2 使用 solvate 添加水

当使用 solvate ↪ 328 对预先构建好的脂质膜进行溶剂化时，你可能会发现水分子会进入膜的空隙中。有几  
种方法可以消除这个问题，包括

- 运行一个短时间的MD，利用脂分子的疏水效应排除这些水分子。一般来说，使用这种方法足以得  
到不含水的疏水相，因为水分子通常会被迅速排出，同时不会破坏膜的一般结构。如果你的设置依  
赖于开始时就完全不含水的疏水相，可以尝试以下建议：
- 设置 gmx solvate ↪ 328 的\-radius选项来更改水的排除半径，
- 将 $GMXLIB位置的 vdwradii\.dat 复制到工作目录，并对其进行编辑，增加脂分子的原子半  
径（建议碳原子的半径在0\.35到0\.5 nm之间），这样脂分子之间的空隙会大大减小，从而避免  
了 solvate ↪ 328 向其中插入水分子。
- 手动编辑结构删除不需要的水分子（记得调整 gro ↪ 610 文件的原子数，并考虑拓扑↪ 617 文件的任何  
变化），或者
- 使用一些脚本删除不需要的水分子。

#### 4\.8\.3 外部材料

- 膜模拟幻灯片↪https://extras\.csc\.fi/chem/courses/gmx2007/Erik\_Talks/membrane\_simulations\.pdf，膜模拟视频↪https:  
//video\.csc\.fi/playlist/dedicated/0\_7z3nas0q/0\_0tr9yd2p\- \(Erik Lindahl\)。
- GROMACS 膜蛋白模拟教程↪http://www\.mdtutorials\.com/gmx/membrane\_protein/index\.html \-旨在展示模拟嵌入  
脂质双层中的蛋白质时出现的问题。
- OPLS\-AA力场与Berger脂分子的联合使用↪http://pomes\.biochemistry\.utoronto\.ca/files/lipidCombinationRules\.pdf \-  
详细的动机，方法和测试。
- 不同力场膜蛋白的一些拓扑gaff，charmm，berger \- Shirley W\. I\. Siu, Robert Vacha, Pavel  
Jungwirth, Rainer A\. Böckmann: Biomolecular simulations of membranes: Physical properties  
from different force fields↪https://doi\.org/10\.1063/1\.2897760。
- Lipidbook↪https://www\.lipidbook\.org/ 是一个脂类，洗涤剂和其他分子力场参数的公共库，可用于模拟膜  
和膜蛋白。其说明见：J\. Domański, P\. Stansfeld, M\.S\.P\. Sansom, and O\. Beckstein\. J\. Membrane  
Biol\. ____236____ \(2010\), 255\-258\. doi:10\.1007/s00232\-010\-9296\-8↪http://dx\.doi\.org/10\.1007/s00232\-010\-9296\-8。

### 4\.9 新分子的参数化

##### 记住以下两条规则，就可以非常简单地解决大多数参数化问题：

##### • 不能混合和匹配力场。力场↪ 63 （最好）是自洽的，一种力场的参数通常不适用于其他力场。如果

##### 你使用一种力场模拟系统的一部分，使用不同的力场模拟系统的另一个部分，而第二种力场的参

##### 数化并没有考虑第一种力场，那么你的结果可能会有问题，并且审稿人会因此产生疑问。选择一种

##### 力场，然后就使用那个力场。

##### • 如果你需要发展新的参数，在导出这些参数时使用的方法需要与力场其他部分最初的导出方式一

##### 致，这意味着你需要查看原始文献。不存在单一正确的方法来导出力场参数；你需要的是导出与力

##### 场的其余部分一致的参数。具体如何操作取决于要使用的力场。例如，对于AMBER力场，导出

##### 非标准氨基酸的参数可能涉及多种不同的量子化学计算，而导出GROMOS或OPLS参数可能涉

及更多\(a\)拟合各种流体和液态属性，以及\(b\)根据经验/化学直觉/类比调整参数。一些自动化方

法的建议可以参考这里↪ 36 。

在尝试参数化新的力场或参数化现有力场的新分子之前，拥有一些GROMACS模拟经验很有必要。这  
些都是非常专业的话题，并不适合（比方说）作为本科生的研究项目，除非你喜欢耗费很多时间却只能  
得到一些随机的数字。你也需要对GROMACS参考手册的第 5 章↪ 524 有非常透彻的了解。如果你觉得  
上面的警告还不够强烈，请阅读以下有关外来物种参数化的内容。

另一条建议：获取参数时不要比购买高级珠宝还随意。只是因为街上的那个家伙愿意以 10 美元的价格  
卖给你一条钻石项链，并不意味着你就应该在那里买一条。同样地，从你从未听说过的人的网站上下载  
你感兴趣分子的参数不一定是最好的策略，特别是如果他们没有解释获得参数的方法的话。

对使用 PRODRG↪http://davapc1\.bioch\.dundee\.ac\.uk/cgi\-bin/prodrg拓扑而不验证其内容的预先警告：讨论这种做法  
不当之处的论文已经 发表↪http://pubs\.acs\.org/doi/abs/10\.1021/ci100335w，论文中还提及了正确导出GROMOS系  
列力场参数的一些提示。

#### 4\.9\.1 外来物种

因此，你想要模拟蛋白质/核酸系统，但它结合了各种外来金属离子（钌?），或者存在对其功能必不可少

的铁硫簇，或者其他类似的情况。但是，（不幸的是?）在你想要使用的力场中没有这些物种的参数。你

该怎么办?

你可以向GROMACS用户论坛↪https://gromacs\.bioexcel\.eu/c/gromacs\-user\-forum/5发送电子邮件，并参考

常见问题解答。

如果你真的坚持要使用分子动力学模拟它们，你需要获得它们的参数，或者从文献中获得，或者通过自

己的参数化得到。但在此之前，可能需要停下来思考一下，因为有时不存在这些原子/团簇的参数是有原

因的。特别是，你可以问下自己以下几个基本问题，看看发展/获取这些物种的标准参数并在分子动力学

中使用它们是否合理，:

- 量子效应（即电荷转移）是否很重要?（也就是说，如果酶的活性位点中含有一个二价金属离子，  
并且你对研究酶的功能感兴趣，这可能是个很大的问题）。
- 对于这种类型的原子/原子团簇，我所选力场使用的标准力场参数化技术可能会失败吗?（即，例  
如由于Hartree\-Fock 6\-31G\*不能充分描述过渡金属）  
如果对这些问题的答案都是肯定的，那么你可能需要考虑使用经典分子动力学以外的其他方法进行模拟。  
即便对这些问题的答案都是否定的，在自己尝试进行参数化之前，你可能需要咨询一下待研究化合物方  
面的专家。此外，在开始这些之前，你可能需要先试着对一些更简单的东西进行参数化。

### 4\.10 平均力势

##### 平均力势（PMF）的定义为，对给定系统的所有构型能给出平均力的势能。在GROMACS中可以使用

##### 几种方法计算PMF，其中最常用的可能是使用牵引代码。使用伞形采样获取PMF可以对统计上不可能

##### 出现的状态进行采样，其步骤如下：

##### • 沿反应坐标生成一系列构型（来自靶向MD模拟，常规MD模拟或一些任意创建的构型）

##### • 使用伞形采样将这些构型限制在采样窗口内。

- 借助 gmx wham ↪ 357 工具，利用WHAM算法重建PMF曲线。  
更详细的教程见 伞形采样↪http://www\.mdtutorials\.com/gmx/umbrella/index\.html。

### 4\.11 单点能

有时候，我们需要计算单个构型的能量。利用GROMACS计算单点能的最佳方法是使用 mdrun ↪ 276 的

\-rerun功能，它可以将 tpr ↪ 619 文件中的相互作用模型用于提供给mdrun的轨迹或坐标文件中的构型。

mdrun\-sinput\.tpr\-rerun configuration\.pdb

注意，提供的构型必须与使用 grompp ↪ 252 生成 tpr ↪ 619 文件时所用的拓扑匹配。除原子名称需要注意外，  
提供给 grompp ↪ 252 的构型无关紧要。此功能也支持能量组（见参考手册↪ 469 ），或者含有多个构型的轨迹  
（在这种情况下， mdrun ↪ 276 默认会为每个构型执行邻区搜索，因为不能假定输入的构型是相似的）。

在输出能量之前进行一次零步数的能量最小化，或者运行一次零步数的MD都需要进行（可避免的）复

杂的处理，这样才能保证在系统含有约束的情况下可以重启，因此不推荐使用这些方法计算单点能。

### 4\.12 碳纳米管

#### 4\.12\.1 Robert Johnson 的提示

摘自Robert Johnson在 gmx\-users邮件列表存档↪https://mailman\-1\.sys\.kth\.se/pipermail/gromacs\.org\_gmx\-users上的帖  
子。

- 绝对要保证拓扑文件中的“末端”碳原子共享一个键。
- 在用于 gmx grompp ↪ 252 的 mdp ↪ 612 文件中使用periodic\_molecules = yes。
- 即使拓扑正确，如果将纳米管置于错误大小的盒子中，也可能发生扭曲，因此可以使用 VMD↪http:  
//www\.ks\.uiuc\.edu/Research/vmd/ 查看纳米管及其周期性映像，确保映像之间的间距正确。如果间距过小  
或过大，会在管中产生大量的应力，从而导致弯曲或伸缩。
- 不要沿纳米管的轴线方向施加压力耦合。事实上，在调试时，最好完全关闭压力耦合，直到你弄清  
楚是否会出现问题，如果出现的话，是什么问题。
- 当将特定的力场用于 x2top ↪ 361 时，会假定分子的连接性。如果是周期性的，纳米管的末端碳原子  
最多只与另外 2 个碳原子成键，或者如果是非周期性的，那么可以使用氢原子封端。
- 你可以使用 x2top ↪ 361 的\-pbc选项生成“无限长”的纳米管。这种情况下， x2top ↪ 361 会识别出末  
端C原子实际上共享一个化学键。因此，当使用 grompp ↪ 252 时，就不会再出现存在单键C原子的  
错误。

#### 4\.12\.2 Andrea Minoia 的教程

使用GROMACS对碳纳米管进行建模（存档见http://chembytes\.wikidot\.com/grocnt）这篇教程中包  
含了使用OPLS\-AA参数对碳纳米管进行简单模拟的所有内容。简单碳纳米管的结构很容易得到，例  
如，可以使用 buildCstruct↪http://chembytes\.wikidot\.com/buildcstruct（Python脚本，也可以添加末端氢原子）或  
TubeGen在线工具↪http://turin\.nss\.udel\.edu/research/tubegenonline\.html （只需将输出的PDB复制并粘贴到文件中  
并命名为cnt\.pdb）。

要使其能够用于GROMACS，你可能需要进行以下操作：

- 创建目录cnt\_oplsaa\.ff
- 在此目录中，使用教程页面中的数据创建以下文件：  
____\-____ 来自 itp ↪ 611 一节的文件forcefield\.itp  
____\-____ 来自 n2t ↪ 614 一节的文件atomnames2types\.n2t  
____\-____ 来自 rtp ↪ 615 一节的文件aminoacids\.rtp
- 使用自定义力场生成拓扑（cnt\_oplsaa\.ff目录必须处于运行 gmx x2top ↪ 361 命令的目录下，或者  
必须能在 GMXLIB路径中找到），运行 gmx x2top ↪ 361 时指定 \-noparam选项，这样就不会使用命  
令行提供的键/键角/二面角的力常数（\-kb，\-ka，\-kd），而是使用力场文件中的值；然而这就  
需要进行下一步（修复二面角的函数类型）

gmx x2top\-f cnt\.gro\-o cnt\.top\-ff cnt\_oplsaa\-name CNT\-noparam

gmx x2top ↪ 361 将二面角的函数类型设置为 1 ，但力场文件指定的类型为 3 。因此，将拓扑文件中\[  
dihedrals \]部分的函数类型 1 替换为 3 。一种方便的修改方法是使用sed（但你的操作系统必须支

持才行；你也可以手动检查top文件并确保只修改了二面角的函数类型）:

sed\-i~'/\[ dihedrals\]/,/\[ system\]/s/1 \*$/3/'cnt\.top

有了拓扑之后，就可以设置系统了。例如，进行简单的真空中的模拟（在em\. mdp ↪ 612 和md\. mdp ↪ 612 中  
使用喜欢的参数）:

放进一个稍微大一点的盒子里：

gmx editconf\-f cnt\.gro\-o boxed\.gro\-bt dodecahedron\-d 1

真空中的能量最小化：

gmx grompp\-f em\.mdp\-c boxed\.gro\-p cnt\.top\-o em\.tpr  
gmx mdrun\-v\-deffnm em

真空中的MD:

gmx grompp\-f md\.mdp\-c em\.gro\-p cnt\.top\-o md\.tpr  
gmx mdrun\-v\-deffnm md

看看轨迹：

gmx trjconv\-f md\.xtc\-s md\.tpr\-o md\_centered\.xtc\-pbc mol\-center  
gmx trjconv\-s md\.tpr\-f md\_centered\.xtc\-o md\_fit\.xtc\-fit rot\+trans  
vmd em\.gro md\_fit\.xtc

### 4\.13 可视化软件

##### 一些可用于可视化轨迹文件和/或坐标文件的程序：

- VMD↪http://www\.ks\.uiuc\.edu/Research/vmd/ \-一个分子可视化程序，可以使用三维图形和内置脚本显示，  
操控和分析大型生物分子系统。可以读取GROMACS轨迹，支持动画。
- PyMOL↪http://www\.pymol\.org \-多功能的分子观察器，支持动画，高质量渲染，晶体和其他常见  
分子图形操作。默认配置无法读取GROMACS轨迹，需要转换为PDB或类似格式。使用  
VMD↪http://www\.ks\.uiuc\.edu/Research/vmd/插件编译时，可以加载 trr ↪ 619 和 xtc ↪ 621 文件。
- Rasmol↪http://www\.umass\.edu/microbio/rasmol/index2\.htm \-其衍生软件 Protein Explorer↪http://www\.umass\.edu/  
microbio/rasmol/ （见下文）可能更好，但Chime组件需要在Windows下运行。Rasmol↪http://www\.  
umass\.edu/microbio/rasmol/index2\.htm可以在Unix上运行。
- Protein Explorer↪http://www\.umass\.edu/microbio/rasmol/\-RasMol↪http://www\.umass\.edu/microbio/rasmol/index2\.htm的  
衍生软件，在研究大分子结构以及结构与功能关系时，这是最容易使用，功能最强大的软件。它可  
以在Windows或Macintosh/PPC计算机上运行。
- Chimera↪http://www\.rbvi\.ucsf\.edu/chimera/ \-一个功能齐全，基于Python的可视化程序，具有各种功能，  
可在任何平台上使用。当前版本可以读取GROMACS轨迹。
- Molscript↪https://github\.com/pekrau/MolScript \-一个脚本驱动的程序，支持以原理图模式和细节表示方法  
高质量地显示分子的三维结构。你可以从Avatar处免费获得学术许可证。

#### 4\.13\.1 拓扑键与呈现键

记住，这些可视化工具只会读取你提供的坐标文件。因此，它们不会使用你的 top ↪ 617 文件或 tpr ↪ 619 文件  
中提供的拓扑信息。进行渲染时，这些程序都会基于自己的猜测显示化学键，因此如果你发现程序给出  
的成键信息并不总是与你的拓扑结构匹配，不要感到惊讶。

Rasmol↪http://www\.umass\.edu/microbio/rasmol/index2\.htm

Protein Explorer↪http://www\.umass\.edu/microbio/rasmol/

Chimera↪http://www\.rbvi\.ucsf\.edu/chimera/

Molscript↪https://github\.com/pekrau/MolScript

### 4\.14 提取轨迹信息

有几种技术可用于在GROMACS轨迹（ trr ↪ 619 ， xtc ↪ 621 ， tng ↪ 617 ）文件中查找信息。

- 使用GROMACS轨迹分析程序
- 使用 gmx traj ↪ 337 输出一个 xvg ↪ 623 文件，并使用外部程序读取此文件，如上所示
- 使用gromacs/share/template/template\.cpp作为模板编写自己的C代码
- 使用 gmx dump ↪ 227 并将shell输出重定向到一个文件，并使用外部程序，如MATLAB，Mathematica  
或其他电子表格软件读取此文件。

### 4\.15 用于轨迹分析的外部工具

##### 近年来，一些外部工具已经足够成熟，可用于分析几个模拟软件包的各种轨迹数据。以下是能够分析

##### GROMACS轨迹数据的已知工具的一个简短列表\(字母顺序\)。

LOOS↪http://loos\.sourceforge\.net/

MDAnalysis↪https://www\.mdanalysis\.org/

MDTraj↪http://mdtraj\.org/latest/index\.html

Pteros↪https://github\.com/yesint/pteros/

### 4\.16 数据绘图

各种GROMACS分析程序都可以生成 xvg ↪ 623 文件。这些文本文件已经过专门格式化，可直接用于  
Grace。但是，对所有的GROMACS分析程序，在运行时你都可以通过使用\-xvg none 选项来禁用  
Grace特定代码的输出。这可以避免gnuplot和Excel等工具的在绘图时出现问题（见下文）。

注意，Grace使用一些嵌入的反斜杠代码来指示单位中的上下标，普通文本等格式。因此，Area  
\(nm\\S2\\N\)中的单位为nm的平方。

#### 4\.16\.1 软件

一些软件包可用于绘制 xvg ↪ 623 文件中的数据：

Grace \-所见即所得的2D绘图工具，用于X Window系统和M\*tif。Grace几乎可以在任何版本  
的类Unix操作系统上运行，前提是你能够解决它的库依赖关系（Lesstif是Motif的一个有效免费  
替代品）。它也可用于其他常见的操作系统。

gnuplot \-可移植的，命令行驱动的交互式数据和函数绘图实用程序，可用于Unix，IBM OS/2，  
MS Windows，DOS，Macintosh，VMS，Atari和许多其他平台。请记住使用：

setdatafile commentschars"\#@&"

以避免gnuplot尝试对 xvg ↪ 623 文件中的特定Grace命令进行处理，或者在运行分析程序时使用

\-xvg none选项。对于简单使用，请执行：

plot"file\.xvg"using 1 : 2 with lines

这是一种能得到正确结果的非常规做法。

- MS Excel \-将文件扩展名改为\.csv并打开文件。出现提示时，选择忽略前 20 行左右并选择固定列  
宽，如果使用德文MS Excel版本，则必须将小数分隔符,改为\.，或使用你最喜欢的\*nix工具。
- Sigma Plot \-一个用于Windows系统的商业工具，包含一些有用的分析工具。
- R \-用于统计计算和图形的自由语言和环境，提供各种统计和图形技术：线性和非线性建模，统计  
检验，时间序列分析，分类，聚类等。
- SPSS \-一个商业工具（Statistical Product and Service Solutions统计产品和服务解决方案），可以  
绘制和分析数据。

### 4\.17 胶束团簇化

##### 如果你得到了完全形成的单个聚集体，并且想获得聚集体或其周围溶剂分子的空间分布函数，那么这个

步骤对于 gmx spatial ↪ 333 工具是必需的。

在计算诸如回旋半径和径向分布函数等性质之前，必须对胶束进行团簇化以确保它不会在周期性边界条  
件↪ 57 的边界处发生断裂。如果不进行这个步骤，得到的结果是错误的（这种错误的一个标志是，可视化  
轨迹看起来正常，但计算的值会出现无法解释的巨大波动）。

需要三个步骤：

- 使用 trjconv ↪ 343 \-pbc cluster获得单个帧，其中所有脂质都处于单元格中。这必须是轨迹的第一  
帧。不能使用以前某个时间点的类似帧。
- 使用 grompp ↪ 252 根据上一步输出的帧创建一个新的 tpr ↪ 619 文件。
- 利用新的 tpr ↪ 619 文件，使用 trjconv ↪ 343 \-pbc nojump生成所需的轨迹。

更明确地说，执行的命令为：

gmx trjconv\-f a\.xtc\-o a\_cluster\.gro\-e0\.001\-pbc cluster  
gmx grompp\-f a\.mdp\-c a\_cluster\.gro\-o a\_cluster\.tpr  
gmx trjconv\-f a\.xtc\-o a\_cluster\.xtc\-s a\_cluster\.tpr\-pbc nojump

### 4\.18 恒 pH 模拟

首先，检查一下你的假定。理想情况是使用恒pH算法来进行MD模拟。然而，传统的显式溶剂MD算  
法无法做到这一点，因为它们使用的是恒H\+算法。此外，如果使用MM力场，那么溶质的位点不可能  
发生质子化/去质子化：游离的H\+会四处运动，而可滴定位点的质子化状态始终保持不变。要解决这  
个问题必须使用非MM的哈密顿量，这样才能支持明确的质子转移。在任何情况下，无论使用什么样的  
哈密顿量，H\+的量都不会改变。  
如果要进行显式溶剂的恒pH模拟，最简单的方法是仍然使用常规MD，但选择特定的H\+数量，并保  
证选择的值对体系而言足够“典型”。此外，需要使用的水分子的数目一般比常规MD模拟中的高几个  
数量级。基本上，对大多数pH值（甚至是pH=4时）都可以忽略游离的H\+浓度，因为其浓度比其他  
抗衡离子（例如Na\+，Cl\-）的浓度低几个数量级。此外，如上所述，单纯的MM哈密顿量无法在可滴  
定位点之间移动质子（这一点与EVB不同），因此你实际上需要为分子中的每个可滴定位点选择质子化  
状态。  
通过对初始结构进行标准的pKa计算，可以很好地估计出分子的初始质子化状态。这是一种常规做法，主  
要利用连续介质静电方法计算质子化自由能（例如，可以使用MEAD↪http://www\.teokem\.lu\.se/~ulf/Methods/mead\.  
html，UHBD↪http://adrik\.bchs\.uh\.edu/uhbd\.html，DelPhi↪http://wiki\.c2b2\.columbia\.edu/honiglab\_public/index\.php/Software:DelPhi，  
APBS↪http://apbs\.sourceforge\.net/等程序），并使用蒙特卡罗方法对质子化状态进行采样（例如，可以  
使用REDTI↪http://www\.msg\.ucsf\.edu/local/programs/mead/mead\.html，PETIT↪http://www\.itqb\.unl\.pt/Research/Associated\_Lab/  
Molecular\_Simulation/Resources/?link=1）。不幸的是，由于溶质的构象会随MD模拟的进行而变化，并且在许多  
情况下存在强的质子化\-构象耦合，质子化状态可能会变得不够。对此已经提出了几种解决方案，但其中  
的大多数或多或少都是启发式的尝试。真正令人满意的解决方案是采用恒pH的MD方法，对此最近几  
年已经提出了一些方法。GROMACS用户邮件列表中对此进行过讨论（请注意，Phil Hunenberger的方  
法存在严重的理论问题）。不幸的是，恒pH方法是最近才出现的，并且仍处于开发和/或测试阶段。希  
望它们在不久的将来会成为标准方法。也许有一天你可以在GROMACS的\.mdp文件中指定pH = 7\.0，  
然后在MD运行过程中就可以看到质子化状态的变化\!在此之前，最好的解决方案可能是上面提到的：  
使用标准pKa计算获得初始质子化状态的良好估计，最后再通过MD快照进行检查。  
Charlie Brooks和其他人开发了恒pH模拟的模型，你可以使用它模拟质子从一个侧链转移到另一个侧  
链的过程。到目前为止，这种方法只能用于隐式溶剂（在CHARMM中也是如此）。  
还有其他几种恒pH的MD方法，其中一些使用显式溶剂。Antonio Baptista组开发了一种基于随机质子  
化状态变化的恒pH MD方法（J\. Chem\. Phys\. \(2002\) 117:4184）。尽管该方法使用了Poisson\-Boltzmann  
方法来周期性地改变质子化状态，但MM/MD模拟使用显式溶剂进行。  
他们实际上使用GROMACS实现了这种随机恒pH MD方法（J\. Phys\. Chem\. B\(2006\)110: 2927），  
基本上就是一种断断续续的分段模拟方法，使用bash和awk脚本将GROMACS与MEAD↪http:  
//www\.teokem\.lu\.se/~ulf/Methods/mead\.html（Don Bashford开发的PB求解器）和MCRP↪http://apo\.ansto\.gov\.au/dspace/  
handle/10238/259（使用蒙特卡罗方法对质子化状态进行采样的自研程序）组合起来。不幸的是，整个操作  
过程在某些地方过于混乱且难以定型，使得它不适合整合到GROMACS中，至少现在是这样。  
Hunenberger提出了另一种仅基于MM/MD的显式溶剂方法（J\. Chem\. Phys\. \(2001\)114: 9706），但其  
理论基础似乎是错误的（J\. Chem\. Phys\. \(2002\) 116:7766）。据我所知，迄今为止提出的所有其他恒pH  
MD方法实际上都使用了隐式溶剂。McCammon（J\. Comput\. Chem\. \(2004\) 25:2038）和Antosiewicz  
（Phys\. Rev\. E\(2002\)66: 051911）使用了隐式溶剂的随机方法，Baptista组还提出了一种分数电荷方法  
（Proteins \(1997\) 27: 523），并使用隐式溶剂来加快计算速度。所有这些方法都依赖于某种简化的静电  
方法（Poisson\-Boltzmann模型，广义Born模型等）来执行质子化状态计算。Brooks（Proteins \(2004\)  
56:738）也提出了一种使用隐式溶剂的方法，采用了一种不同但理论含糊的方法来考虑质子化效应。

有关可解离水模型的讨论，可以参考这篇论文↪http://dx\.doi\.org/10\.1021/jp072530o。

注：以上内容来自GROMACS用户邮件列表中的一些电子邮件，但大部分出自Antonio Baptista。

### 4\.19 扩散系数

利用GROMACS轨迹，你可以根据爱因斯坦方程↪https://en\.wikipedia\.org/wiki/Einstein\_relation\_\(kinetic\_theory\)（gmx  
msd）或Green\-Kubo方程↪https://en\.wikipedia\.org/wiki/Green%E2%80%93Kubo\_relations（gmx velacc，gmx analyze）  
来计算扩散系数。gmx msd的使用非常简单，但从4\.0版本开始gmx velacc的使用有点棘手。

要通过Green\-Kubo方程计算粒子的扩散系数，首先使用以下命令：

gmx velacc \-acflen 1001 \-nonormalize \-mol \-n atoms\.ndx \-s topol\.tpr

其中atoms\.ndx应包含要计算扩散系数的粒子的原子数目。默认情况下，程序会在vac\.xvg中输出线性  
速度自相关函数（VACF）。

然后再输入下面的命令：

gmx analyze \-f vac\.xvg \-integrate

执行成功后会得到VACF的积分，单位为nm^2 /ps。

最后，如果VACF的积分值为 6 × 10 \-5nm^2 /ps，将该值乘以 10 \-6（将nm^2 转换为m^2 ，同时将ps转换  
为s）并除以 3 （根据Green\-Kubo方程），得到 2 × 10 \-11m^2 /s。这就是扩散常数的值。

### 4\.20 二面角主成分分析（ PCA ）

要创建二面角PCA↪http://www\.gromacs\.org/Documentation/Terminology/Principal\_Components\_Analysis的索引文件，请使  
用gmx mk\_angndx或手动创建索引文件。然后，你需要适当地组合gmx angle（可能需要\-oc或\-or选  
项）和gmx covar。

这里有关于二面角PCA使用的一些讨论↪http://dx\.doi\.org/10\.1002/prot\.20900和答复↪http://www\.ntu\.edu\.sg/home/ygmu/  
reply\_from\_mu\_stock\_phuong\.pdf。

#### 4\.20\.1 GROMACS 中 PCA 的实现

首先创建一个降维的轨迹文件，使其与所选角度匹配，然后创建一个包含特征向量和特征值的伪轨迹文

件。这可能不是最好的方法，但确实可行。下面的步骤 1 和 2 进行降维，步骤 3 和步骤 4 生成一种魔改

过坐标文件，其维数足够大，以便能够用于gmx covar和gmx anaeig。

具体步骤如下：

1\.使用gmx mk\_angndx或文本编辑器为选定的二面角所涉及的原子生成索引文件。

2\.使用步骤 1 中的索引文件（例如angle\.ndx）从轨迹中提取角度，命令如下：

gmx angle \-f foo\.xtc \-s foo\.tpr \-n dangle\.ndx \-or dangle\.trr \-type dihedral

输出文件dangle\.trr中包含了所选角度维度的模拟轨迹。

3\.创建一个名为covar\.ndx的索引文件，其中必须包含一组从 1 到整数\(2\*N/3\)的原子，其中N为

二面角的数量。例如，对于含有 5 个二面角的肽，covar\.ndx的内容应为

\[ foo \]

1 2 3 4

4\.使用索引文件生成包含整数\(2\*N/3\)个原子的\.gro文件。盒子大小和原子坐标无关紧要。例如，

gmx trjconv \-s foo\.tpr \-f dangle\.trr \-o resized\.gro \-n covar\.ndx \-e 0

5\.使用如下命令执行对角化

gmx covar \-f dangle\.trr \-n covar\.ndx \-ascii \-xpm \-nofit \-nomwa \-noref \-nopbc \-s␣

↪resized\.gro

输出为eigenval\.xvg，eigenvec\.trr，covar\.log，covar\.dat和covar\.xpm。

6\.要获得沿某个特征向量的PMF，请使用类似如下的命令

gmx anaeig \-v eigenvec\.trr \-f dangle\.trr \-s resized\.gro \-first X \-last X \-proj␣

↪proj\-1

其中X为特征向量的序号。要可视化结果，请使用

xmgrace proj\-X\.xvg

7\.要获得沿两个特征向量投影的自由能形貌图，请使用类似如下的命令

gmx anaeig \-v eigenvec\.trr \-f dangle\.trr \-noxvgr \-s resized\.gro \-first X \-last Y␣

↪\-2d 2dproj\_X\_Y\.xvg

其中X和Y为特征向量的序号。

8\.要将这些数据转换为自由能形貌图，需要使用网格划分2D形貌并计算每个网格内的构象数。gmx

sham程序（指定\-notime选项）也可用于生成自由能曲面的2D图。

### 4\.21 二面限制

从GROMACS 4\.6开始，二面角限制完全在拓扑中指定，删除了以前使用的mdp设置。具体的实现方  
法见手册。

假定peptip\.itp中的原子编号如下

C' \(n\-1\) = 5  
N \(n\) = 7  
CA \(n\) = 9  
C' \(n\) = 15  
N \(n\+1\) = 17

在\.top文件中应该使用如下所示的内容，并将 180 替换为实际的二面角值，也就是你要将原子限制到的  
值（以度为单位）。

\#include "peptide\.itp"  
\[ dihedral\_restraints \]  
; ai aj ak al type label phi dphi kfac power  
; phi C'\(n\-1\) \- N \- CA \- C'  
5 7 9 15 1 1 180 0 1 2  
; psi N \- CA \- C' \- N\(n\+1\)  
7 9 15 17 1 1 180 0 1 2

\#include "tip3p\.itp"  
;其他\.\.\.

确保\[ dihedral\_restraints \]部分紧跟在包含蛋白拓扑（\.itp文件）的语句之后。如果\.top文件中直  
接含有蛋白拓扑，那么只需在该蛋白质列表之后，任何其他分子之前插入\[ dihedral\_restraints \]即  
可。

\[ dihedral\_restraints \]指令中指定的参数如下：

type:限制类型，只能使用 1

label:未使用，后续版本会删除此项

phi:公式中的𝜙 0 值

dphi:公式中Δ𝜙的值

kfac:类似距离限制中的fac，力常数会乘以此系数（在\.mdp文件中指定，参见下文）。这样，即  
使只提供一个dihre\_fc的值，也可以通过不同的力常数来维持不同的限制。

power:未使用，后续版本会删除此项

几点说明：

1\.对于这种类型的二面角限制在 180 度附近是否稳定，手册无清楚说明。Chris Neale发现，在包括

180 度在内的整个二面角范围内，一切模拟似乎都表现正常，且符合预期。然而，必须避免实际二

面角偏离受限制的二面角接近 180 度的情况。

并非所有人都同意以上说法。因此，你需要做一些测试得出自己的结论。

2\.请特别注意单位。GROMACS手册中说明如下：请注意，在拓扑文件的输入中，角度的单位为度，

力常数的单位为kJ mol\-1rad\-2。

### 4\.22 距离限制

通过在拓扑中设置\[ distance\_restraints \]，可以将同一 \[ moleculetype \]中两个原子之间的距  
离限制为指定值。手册中给出了该算法的实现和基本方程。

\[ distance\_restraints \]部分的一个示例如下：

\[ distance\_restraints \]  
; ai aj type index type’low up1 up2 fac  
10 16 1 0 1 0\.0 0\.3 0\.4 1\.0  
10 28 1 1 1 0\.0 0\.3 0\.4 1\.0  
10 46 1 1 1 0\.0 0\.3 0\.4 1\.0  
16 22 1 2 1 0\.0 0\.3 0\.4 2\.5

上述指令指定了原子对（ai和aj）之间的距离限制。使用的项如下：

- type:类型，只能使用 1
- index:索引。具有相同索引值的多个限制可以一起控制。上面示例中第二个和第三个限制一起考  
虑，而第一个和第四个限制是独立考虑的。
- type':可以使用 1 或 2 ;使用 2 表示限制不会进行时间平均或系综平均（用于限制氢键）
- low:公式中r0的值。
- up1:公式和图中R1的值
- up2:公式和图中R2的值
- fac:力常数（\.mdp文件中的disre\_fc）乘以的因子。这样，即使只提供了一个dihre\_fc的值，  
也可以通过不同的力常数来维持不同的约束。

### 4\.23 本性动力学

##### 本性动力学提取蛋白质的相关运动，以了解对蛋白质活动最基本的运动。蛋白质中相关运动的分析可以

通过gmx covar和gmx anaeig来完成。

Interactive Essential Dynamics↪http://mccammon\.ucsd\.edu/ied/提供了使用VMD对本性动力学进行交互可视  
化的示例。

### 4\.24 多条链

##### 要生成用于模拟多个不同分子的拓扑（即PDB中的不同链），我们首先要区分两种情况：不同链的拓扑

##### 完全相同的情况，以及不同链的拓扑不同的情况。

#### 4\.24\.1 完全相同的链

这是简单的情况。获得单链的结构文件后使用gmx pdb2gmx生成拓扑（注意，正常情况下，此结构没有  
必要采用PDB格式）。仔细查看生成的\.top文件，在文件在底部你会看到类似如下的部分

\[ molecules \]  
Protein 1

这说明此分子在前面已被命名为Protein（或其他名称）。你可以将分子数从 1 更改为所需的任何值。然  
后，将此\.top文件与另一个坐标文件（其链数对应于修改后的\.top文件）一起作为gmx grompp的输入。

你可以使用gmx editconf对链进行平移并生成副本，以便稍后拼接到单个文件中。你也可以使用gmx  
genconf生成整个体系的副本。

#### 4\.24\.2 不同的链

##### 这比较棘手。你可以使用一种能够标识不同链的坐标文件格式，例如PDB格式，它可以在第 22 列中指

定一个字母（作为链标识符）。gmx pdb2gmx程序可以识别不同的链标识符，并将它们作为不同的分子  
输出（从而得到单独的拓扑）。例如，链A会对应的拓扑名称为topol\_A\.itp，链B的为topol\_B\.itp，  
依此类推。请注意，在生成的\.top文件中，即使链实际上代表完全相同的分子（即同型二聚体蛋白质），  
每条链也会生成单独的拓扑。

在GROMACS 4\.5中，gmx pdb2gmx的\-chainsep选项可以控制是否以PDB的TER记录作为将链断开  
以便开始新的\[ moleculartype \]部分的依据。

#### 4\.24\.3 是否需要将链分成不同的分子?

##### 注意，为了使用GROMACS进行模拟或分析，没有必要使用单独的链标识符将链划分为不同的分子。

除不同部分之间不能存在成键相互作用之外，GROMACS实际上并不关心\[ moleculetype \]部分中包  
含的内容。你可以创建一个索引文件，其中包含指定链的残基编号。例如，如果你有一个二聚体蛋白，  
每条链包含 200 个氨基酸残基，链A可能对应于残基1\-200，链B对应于残基201\-400。因此，在gmx  
make\_ndx提示符下，可以输入

r 1\-200

选择第一链。输入

选择第二条链。r 201\-400

这样，你可以分别对每条链进行分析，而不必担心链标识符。

### 4\.25 多个拓扑条目

##### 在某些情况下，可能需要生成比标准形式更复杂的成键项。这可以通过组合多个项来实现，然后将这些

项加起来形成最终所需的成键项。例如，当二面角的势函数为Ryckaert\-Bellemans函数，但附加项无法  
使用GROMACS中标准的n=5形式时，可以使用这种方法。

拓扑文件中\[ bonds \]，\[ pairs \]，\[ angles \]和\[ dihedrals \]部分的条目具有加和性，每个额  
外是条目会累加到之前的项上。在这些地方重复某一项会导致势能项加倍（不会给出警告信息\!），因此  
请谨慎修改。

不要将此机制与ffbonded\.itp文件中键类型的定义（即\[ bondtypes \]，\[ angletypes \]和\[  
dihedraltypes \]）混淆；对于那些指令，最后一项会覆盖前面的项，并导致gmx grompp失败并给  
出警告。但CHARMM力场不遵循这一规则。

### 4\.26 简正模式分析

##### 运行简正模式分析是为了研究大分子（通常是蛋白质）潜在的大尺度的功能性运动。这种计算需要进行

非常彻底的能量最小化并计算Hessian矩阵。

通常，对于最终阶段的能量最小化（使用L\-BFGS）和实际的简正模式分析，你都可以使用

- 双精度的GROMACS
- 切换库仑和范德华相互作用；例如，截断值取1\.0 nm，从0\.8 nm开始切换（或从0 nm偏移）
- rlist在1\.2到1\.3 nm范围内

在创建简正模式的运行输入文件时，必须使用\-t选项来执行gmx grompp，这样就可以读取全精度的二  
进制坐标，而不是 3 位小数的十进制\.gro文件。

### 4\.27 聚合物

GROMACS非常适合对聚合物材料进行模拟。在gmx\-users用户邮件列表上经常询问的问题之一是，如  
何为包含许多重复单元的聚合物创建拓扑。最简单的方法可能是为所需的力场创建\.rtp条目，然后使  
用gmx pdb2gmx创建拓扑。

为此，至少需要定义三种残基类型：

1\.“起始”残基，定义了链的“开始”  
2\.重复的（内部）残基  
3\.“末端”残基，定义链的“末端”  
这里↪http://mailman\-1\.sys\.kth\.se/pipermail/gromacs\.org\_gmx\-users/2009\-March/040125\.html有一个如何实现的具体示例，处理  
的是OPLS\-AA力场中的聚乙烯。

一些在线服务器允许用户构建某些类型的聚合物，虽然不能解决构建拓扑的问题，但对于生成材料的初  
始坐标还是有用的。

### 4\.28 位置限制

##### 位置限制算法用于将粒子/原子限制在固定的参考位置。因此，原子可以移动，但偏离预定位置会导致体

##### 系的能量剧增。

##### 使用位置限制的原因有：

##### • 避免体系的关键部分发生剧烈的位置变化，例如在对添加的溶剂进行平衡过程中限制住蛋白质。

##### • 对因缺失粒子而没有恰当相互作用的区域，可使用受限制的粒子壳层将要研究的区域与外部区域

##### 隔离开（GROMACS尚未实现）。

可以将位置限制部分添加到拓扑文件中，并在需要时利用包含文件机制将其激活。如果使用gmx  
pdb2gmx，使用\-i选项可以将非氢原子写入posre\.itp文件，然后将其包含在拓扑文件中。你可以通过  
在\.mdp文件中设置define = \-DPOSRES选项来控制实际上是否读取上述位置限制文件。

位置限制部分必须物理上位于要限制的\[ moleculetype \]中。\.top文件中不能包含全局位置限制部分。  
具体请参阅相关的错误信息。

可以使用gmx genrestr程序创建特殊的位置限制\.itp文件。例如，如果你希望仅对蛋白质的骨架  
原子应用位置限制，请使用gmx genrestr，选择Backbone作为输出组，并在拓扑中使用\#include  
"backbone\_posre\.itp"。

#### 4\.28\.1 示例

位置限制需要以下信息，这些信息要放在拓扑文件（\.top或\.itp）中：

- 标识要应用的原子/粒子（在\[ moleculetype \]内而不是坐标文件内）
- 函数类型
- 每个维度\(x, y, z\)上的力常数

\[ moleculetype\]  
第一个分子

\[ position\_restraints \]

; ai funct fcx fcy fcz

1 1 1000 1000 1000 ; 限制在一个点

2 1 1000 0 1000 ;限制在一条线（y轴）

2 1 1000 0 0 ; 限制在一个面（y\-z平面）

\[ moleculetype \]  
第二个分子  
\.\.\.  
\[ position\_restraints \]  
; ai funct fcx fcy fcz  
1 1 1000 1000 1000 ; 限制在一个点  
2 1 1000 0 1000 ;限制在一条线（y轴）  
2 1 1000 0 0 ; 限制在一个面（y\-z平面）

; 请注意，原子索引ai是相对于当前\[ moleculetype \]的，而不是相对于整个坐标文件的

更多信息请查看手册中位置限制实现的公式

如何在分子拓扑文件中实现位置限制的

### 4\.29 使用 Fortran 读取 XTC 文件

gmx\-users用户邮件列表中有很多关于使用Fortran程序读取\.xtc文件的问题。那里给出了两三个解决  
方案，可以使用的一种方法是利用VMD的molfile插件。

基本上，你需要下载VMD源代码并编译molfile插件（不需要编译VMD本身）。它只需要很少的依赖  
项（TCL和NETCDF），并且不需要额外的技巧。此外，这种方法不使用xdr库，因为插件以某种方式  
模拟了这个库的功能，因此我们也不需要xdr库。

先编译位于plugins/molfile\_plugin/f77目录中的Fortran测试程序，它展示了如何使用插件。这可  
能有点棘手，并且需要对Makefile进行一些处理（将f77更改为gfortran等）。针对我的情况（Ubuntu  
7\.10），必须通过建立指向所需文件的符号链接来应对不兼容的libstdc\+\+。

然后编译你自己的测试程序，并试着读取xtc文件。实际上你还可以读取VMD支持的任何格式。不过，  
这种更改不支持输出\.xtc文件（以及其他格式）。

### 4\.30 减少轨迹文件的存储空间

##### 此建议还适用于由于（实际）内存不足而导致分析工具崩溃（或速度太慢）的情况。

首先，考虑下你输出的轨迹是否远多于需要保存的。查看\.mdp文件选项，了解\.trr文件中位置的输出频  
率（Nstxout）和速度的输出频率（Nstvout），是否应使用\.xtc文件（Nstxtcout）以可选的低精度更  
有效地存储位置信息，以及是否应该只输出体系一部分的坐标（xtc\_grps）。

你不需要保存每一帧，因为每帧与其相邻帧之间的相关性很强。如果你确定不会对溶剂坐标进行分析，  
就没有必要保存它们，通常它们的数目远远超过要研究的溶质。因此，如果后面分析时只需要溶质的位  
置数据，那么可以只将溶质组输出到\.xtc文件（xtc\_grps）中，并且保存频率（Nstxtcout）与所需要  
的一样高，这样做相比输出整个体系每一步位置和速度信息的\.trr文件，占用的空间要小得多。

可以使用\.trr文件进行重启，因为它们是独立的。请注意，如果分析过程中需要计算自相关函数，那么

保存的频率要比高于体系的特征时间。

对于GROMACS 3\.x，用户通常只希望\.trr文件能提供一个完整的包含位置和速度的帧，保存的频率只

要能够保证重启即可\(同时确保能量输出频率（nstenergy\)是合适的倍数，以保证重启时有相应帧的能

量），该频率通常比你希望输出数据进行分析的频率小得多。

在GROMACS 4\.x及更高版本中，检查点文件中包含了用于重新启动模拟的位置，速度和能量的所有信

息。

请注意，你也可以在执行模拟完成后使用gmx trjconv和gmx eneconv来降低输出频率，更改文件格式

和选择输出组，但最好在模拟之前（正确地\!）做出这些决定。

### 4\.31 副本交换分子动力学

相对于标准的分子动力学模拟，副本交换分子动力学（REMD）是一种增强采样的技术，采用的方法是

在不同温度下对具有相似势能的体系进行采样。通过这种方法，体系可能会越过势能面上的能垒，从而

探索新的构象空间。

实际上，REMD模拟的设置非常简单。下面给出对指定体系运行REMD模拟的步骤。至于模拟是否

“成功”完全取决于要解决的问题和判断成功的标准。虽然REMD模拟可以增加采样量，但并不能提供

最终答案。这一点应该牢记在心。

一旦确定了多肽及其周围环境，就需要确定待采样温度空间的范围，使用的处理器数目以及模拟的时间

长度。体系，副本数目，温度空间的范围和温度分布决定了副本之间的平均交换概率。这些值对所有副

本都应该是相同的。为此，如果假定自由能空间中没有已知的瓶颈部分，预期体系的势能会随温度的增

加而增加，因此副本的温度分布应服从指数分布

有充分的证据表明，对多肽/蛋白质体系，副本尝试交换的时间间隔不应小于1 ps。这可以决定在两

次交换之间，一个副本探索相应构象空间所用的平均时间，这个时间比实际的交换概率还重要。在

GROMACS的实现中，特定一对副本的交换尝试会隔次进行，因为奇数对和偶数对尝试交换会交替进

行。

对低于4\.0版本的GROMACS，只允许每个副本使用一个处理器。要运行REMD，任何版本的

GROMACS都必须使用MPI进行编译mdrun（即不能使用线程并行），并且处理器的数目应该是副本

数目的倍数。

4\.31\.1 一般步骤

1\.定义体系，例如：多肽\+溶剂（隐式或显式）。GROMACS 4\.5及以上版本才支持隐式溶剂。

2\.根据可用的处理器数目和要采样的温度范围（实际上它们的相关性非常强），选择温度分布。使用

指数分布：𝑇𝑖= 𝑇 0 𝑒𝑘∗𝑖，其中𝑘和𝑇 0 可以微调以获得合理的温度间隔保证能够进行交换。指数形

式可以保证温度间隔随温度升高而增大。这是必要的，因为总能量的分布随着温度的增加而增加，

因此交换概率也随之增加。保持交换概率不随温度变化。

3\.获得温度分布后，在N个温度下分别对体系进行平衡（每个温度使用单独的\.mdp文件）。然后根据

平衡结构创建一系列（N个）运行输入文件（\.tpr），仍要使用不同的\.mdp文件生成不同的\.tpr文

件。如果有N个温度应该创建N个\.tpr文件，名称依次为prefix\_0\.tpr，\.\.\. prefix\_N\-1\.tpr。

1. 然后，运行短时间的REMD模拟以获得交换概率的估计值（大约100 ps就可以获得良好的估计

值），如果得到的结果与所需值偏离较大，试着修改温度。典型情况下，交换概率取0\.2到0\.3是

合适的。实际上，比交换概率本身的值更重要的是副本在给定温度下的停留时间。它的值为交换概

率与交换频率的乘积。例如，交换概率为0\.2，每隔2 ps进行一次交换尝试，可以得出相应温度下  
的平均时间为10 ps。另外还需要考虑的是交换方式。每次尝试时，是尝试交换所有的副本对，还  
是随机选择一对副本进行交换。对后一种情况，还应考虑一点，必须将副本的停留时间乘以N\-1，  
即交换对的数目。  
5\.每个温度下的初始构象可以相同，也可以不同。如何选择取决于运行REMD的原因。  
网上↪http://virtualchemistry\.org//remd\-temperature\-generator/index\.php有一个可以选择T\-REMD温度的在线工具，它  
是基于溶剂化蛋白已知的能量分布计算的。输入蛋白质的原子数，水的原子数，温度范围和所需的交换  
概率，这个工具就会生成所需的温度。

#### 4\.31\.2 具体步骤

1\.创建一组\.mdp文件，每个文件指定要使用的不同温度。根据索引对得到的\.tpr文件进行编号，

从 0 到任意数字（例如，如果有 10 个不同的温度，则名称为prefix\_0\.tpr，prefix\_1\.tpr\.\.\.

prefix\_9\.tpr）。对GROMACS 4\.0之前的版本，每个副本只能使用一个处理器，因此要么

省略gmx grompp的\-np选项，要么使用\-np 1。对于GROMACS 4\.0，gmx grompp时不需要使

用\-np选项。

2\.副本交换的间隔由mdrun选项\-replex指定。计算所用的核心数必须是副本数的倍数（由\-multi给

出，必须等于\.tpr文件的数目，对于上面的示例，使用prefix\_0\.tpr至prefix\_9\.tpr，此数目为

10 ）。如上所述，对于4\.0版之前的GROMACS，该倍数必须为 1 。输入文件的命名对于mdrun的

正确运行至关重要。

3\.命令行示例参见下文。运行步数是要达到所需的交换尝试周期所需的步数。可能还需要其他命令

行选项，例如\-o prefix

GROMACS 3\.x: mpirun \-np 10 mdrun \-s prefix\_\.tpr \-np 10 \-multi 10 \-replex（步数）（后  
接输出选项）

GROMACS 4\.x: mpirun mdrun \-s prefix\_\.tpr \-multi 10 \-replex（步数）（后跟输出选项）

#### 4\.31\.3 理解 REMD 相关的输出

mdrun会将重要信息输出到md\.log文件，你可以像这样提取它：

grep Repl md0\.log

Initializing Replica Exchange  
Repl There are 6 replicas:  
Repl 0 1 2 3 4 5  
Repl T 300\.0 350\.0 410\.0 480\.0 560\.0 650\.0  
Repl  
Repl exchange interval: 1000  
Repl random seed: 525106  
Repl below: x=exchange, pr=probability  
Replica exchange at step 1000 time 2  
Repl 0 <\-> 1 dE = 2\.492e\+00  
Repl ex 0 1 2 3 4 5

Repl pr \.08 \.00 \.13

Replica exchange at step 2000 time 4

Repl ex 0 1 2 3 x 4 5

Repl pr \.00 1\.0

这些解释确实很简略，希望它能够提供足够的信息来帮助你理解得到的结果。

#### 4\.31\.4 后处理

##### GROMACS输出的REMD轨迹是系综连续的，但相对于模拟时间却不连续。如果需要后者，可以使用

脚本scripts/demux\.pl读取md0\.log文件（必要时可以合并多个文件），生成一些输出文件。其中之一  
是\.xvg文件（replica\_ndx\.xvg），trjcat可以使用该文件和原始轨迹文件得到连续轨迹。另一个文件  
（replica\_temp\.xvg）包含了每个副本从原始温度开始的温度。因此，如果感兴趣的副本开始于，比方  
说，300 K，你可以在温度空间中跟踪它的轨迹。如果能给出每个副本的温度分布直方图可能更好，根  
据大多数作者的说法，这种直方图应该是平坦的。使用这种方法处理过的轨迹已经用在论文中了，可  
以根据REMD轨迹获得蛋白质的折叠动力学Rev\. Lett\. 96, 238102 \(2006\)。（在g\_kinetics中实现\-在  
GROMACS 3\.3\.1或更早版本中不可用）

### 4\.32 表格势能

#### 4\.32\.1 非键的表格相互作用

对于Buckingham势，𝑓 \(𝑟\)和𝑔\(𝑟\)是相同的，但ℎ\(𝑟\) = 𝐴𝑒−𝐵𝑟。

参数𝐴，𝐵和𝐶来自拓扑中的值。相互作用的类型是Lennard\-Jones还是Buckingham由拓扑的\[

defaults \]指令中的nbfunc参数确定。

要利用自定义的势能，需要注意以下几点：

1\.正确设置\.mdp文件中的vdwtype和coulombtype。vdwtype应设置为user，coulombtype可以

是user，pme\-user，pme\-user\-switch中的任一项。

2\.包含与上述函数值的适当table\.xvg文件。更多信息见下文。

3\.在GROMACS 4\.6和5\.0版本中，需要使用cutoff\-scheme=Group，因为Verlet方案尚未实现用

户表格势能。

##### 构造表格

表格的间距（即r值之间的间距）必须均匀。对于单精度GROMACS，0\.002 nm的间距就足够了。对于  
双精度，请使用0\.0005 nm。对于table\.xvg文件中未给出的值，GROMACS会使用三次样条曲线方法  
进行插值。r的最大值必须大于rc \+ 1，其中rc是\.mdp文件中定义的最大截断距离。可以在GROMACS  
安装路径下的/share/gromacs/top子目录中找到一些示例表格。

以下Fortran代码可以生成一个9\-6表（即/share/gromacs/top中的table6\-9\.xvg）:

program gen\_table  
implicit none  
real,parameter :: delr=0\.002,rcut=1\.0  
real :: r  
integer :: nbins,j  
nbins=int\( \(rcut\+1\)/delr\) \+ 1  
do j=0,nbins  
r=delrj  
write\(6,\) r, 1/r, 1/\(rr\), \-1/r6, \-6/r7, 1/r9, 9/r\*10  
end do  
end

以下C代码可以生成6\-12表（table6\-12\.xvg）:

\#include <stdio\.h>  
\#include <math\.h>  
main\(\)

FILE \*fout;

double r;

fout = fopen\("table\_example\.xvg", "w"\);

fprintf\(fout, "\#\\n\# Example LJ 6\-12 Potential\\ n\#\\ n"\);

for \(r=0; r<=3; r\+=0\.002\)

double f = 1/r;

double fprime = 1/\(pow\(r,2\)\);

double g = \-1/\(pow\(r,6\)\);

double gprime = \-6/\(pow\(r,7\)\);

double h = 1/\(pow\(r,12\)\);

double hprime = 12/\(pow\(r,13\)\);

/\* print output \*/

if \(r<0\.04\)

fprintf\(fout, "%12\.10e %12\.10e %12\.10e %12\.10e %12\.10e %12\.10e %12\.

↪10e\\ n", r,0\.0,0\.0,0\.0,0\.0,0\.0,0\.0\);

else

fprintf\(fout, "%12\.10e %12\.10e %12\.10e %12\.10e %12\.10e %12\.10e %12\.

↪10e\\ n", r,f,fprime,g,gprime,h,hprime\);

fclose\(fout\);

return\(0\);

请注意，当r=0时，表格势能的值无限大或未定义。上面的C代码将所有r < 0\.04 nm的函数值都设定  
为零，如示例表（/share/gromacs/top/table6\-12\.xvg）一样，绝对必需的唯一值是r = 0。

##### 使用方法

##### 以下示例体系中有两种粒子类型，分别为A和B。拓扑中指定了两种粒子类型的非键参数（对于LJ势，

为A和C;对于Buckingham，为A，B和C）。指定grompp（最终是mdrun）使用表格势能，请设置  
以下内容：

vdwtype = User  
coulombtype = User  
energygrps = A B  
energygrp\_table = A A B B

这样mdrun运行时需要三个文件：table\.xvg（用于AB相互作用），table\_A\_A\.xvg（用于AA相互  
作用）和table\_B\_B\.xvg（用于BB相互作用）。如果必要，必须在运行grompp之前为A和B构建适  
当的索引组。

更多详细说明和一些示例，请参阅Gareth Tribello的文档。

### 4\.33 在脚本中使用命令

##### GROMACS程序通常是交互式的，可以在程序启动后选择索引组。

在shell脚本中，有两种方法可以使程序以非交互方式执行（以g\_rms为例）:

1\.命令行

2\.在脚本内

3\.使用组名

4\.复杂示例

##### 命令行

echo 3 3 | g\_rms \-flags

####  使用组名

##### 有时某些选择的编号可能因情况而异，因此在GROMACS 3\.3\.1及更高版本中，可以将名称明确地传递

##### 给工具。

g\_energy \-f ener\.edr << EOF  
Pot  
Kin  
Tot  
EOF

程序会使用最佳匹配，例如，如果你选择Pres，程序会使用以Pres开头的第一个项。

### 4\.34 使用 VMD 插件读取非 GROMACS 原生的轨迹格式

##### 如果已经安装了VMD（版本>=1\.8\.6），并且你的机器支持动态加载，那么从4\.0\.7版本开始，所

##### 有的GROMACS工具都可以读取VMD支持的任何轨迹文件格式（例如AMBER的DCD格式）。

可以将VMD\_PLUGIN\_PATH环境变量设置为VMD安装目录下的molfile文件夹，如果VMD安装在了  
标准位置，也可以自动找到该文件夹 。如果这样，任何GROMACS工具都可以使用file\.dcd而不  
是file\.trr。

自GROMACS 4\.6版本后，CMake能够检测VMD并确定是否可以使用插件。这样就不需要在运行时  
设置环境变量，但是如果需要，VMDDIR和VMD\_PLUGIN\_PATH环境变量可分别指向VMD安装目录和/或

其molfile文件夹。

GROMACS和VMD都需要同时编译为 32 位或 64 位，而且GROMACS工具无法使用VMD插件输  
出文件。

## 第 5 章分子动力学参数（\.mdp选项）

### 5\.1 通用信息

##### 参数的默认值或者在括号中给出，或者是第一个列出的选项。列表中的第一个选项始终是默认选项。方

##### 括号中给出单位。选项中的短划线和下划线没有区别，可互相替换。

这里有一份示例 mdp 文件↪ 612 。可用于启动一个常规模拟。你可以在它的基础上添加或修改，以满足自  
己的特定需求。

### 5\.2 预处理

include

在拓扑中包含特定的目录，GROMACS搜索需要的文件时会使用这些目录。格式：\-I/home/john/

mylib \-I\.\./otherlib

define

传递给预处理器的定义，默认不存在。可以使用任何定义，用于控制自定义拓扑文件中的选项。已

有 top ↪ 617 文件默认可用的选项包括

\-DFLEXIBLE:在拓扑中使用柔性水模型而不是刚性水模型，用于简正模式分析。

\-DPOSRES:使用拓扑中的包含posre\.itp文件，用于位置限制。

### 5\.3 运行控制

integrator

（尽管名称的意思为积分方法，但此参数实际上包括了不属于时间积分的算法。

integrator=steep ↪ 124 及其后面的所有条目都是如此）

md

使用蛙跳式算法积分牛顿运动方程。

md\-vv

使用速度Verlet算法积分牛顿运动方程。对于从同一轨迹中的对应点开始的恒NVE模拟，

此方法得到的轨迹与使用 integrator=md ↪ 124 的蛙跳式方法得到的轨迹，在解析的角度上是

等同的，但并非二进制等同。由于动能是根据整个积分步的速度计算的，因此略偏高。这种

积分方法的优点是，更精确，可逆的基于Trotter展开的Nose\-Hoover和Parrinello\-Rahman

耦合积分，以及（稍偏小的）整步速度输出。这些优点的代价是额外的计算量，特别是约束

和并行中的额外通信。注意，对于几乎所有的成品模拟， integrator=md ↪ 124 积分方法都足

够精确。

md\-vv\-avek

等同于 integrator=md\-vv ↪ 124 的速度Verlet算法，但动能是 integrator=md ↪ 124 积分方法

的两个半步动能的平均值，因此更精确。当与Nose\-Hoover和/或Parrinello\-Rahman耦合联

用时，计算成本略有增加。

sd

准确，高效的跳蛙式随机动力学积分方法。使用约束时，每个积分步需要对坐标进行两

次约束。取决于力的计算成本，这可能会占用相当一部分模拟时间。一组或多组原子

（ tc\-grps ↪ 137 ）的温度可通过 ref\-t ↪ 137 设置，每组的逆摩擦系数由 tau\-t ↪ 137 设定。忽

略 tcoupl ↪ 136 和 nsttcouple 参数。使用 ld\-seed ↪ 126 初始化随机数生成器。当用作恒温器

时， tau\-t ↪ 137 的适当值为2 ps，因为这样得到的摩擦低于水的内部摩擦，同时又高到足以

去除多余的热量。注意：温度偏差的衰减速度是使用相同 tau\-t ↪ 137 的Berendsen恒温器的

二倍。

bd

用于布朗或位置 Langevin动力学的欧拉积分方法，粒子速度为其受力与摩擦系数

（ bd\-fric ↪ 126 ）的比值，再加上随机热噪声（ ref\-t ↪ 137 ）。当 bd\-fric ↪ 126 为 0 时，每

个粒子的摩擦系数为质量和 tau\-t ↪ 137 的比值，与 integrator=sd ↪ 124 积分方法类似。使

用 ld\-seed ↪ 126 初始化随机数生成器。

steep

用于能量最小化的最陡下降算法。最大步长为 emstep ↪ 127 ，容差为 emtol ↪ 127 。

cg

用于能量最小化的共轭梯度算法，容差为 emtol ↪ 127 。如果每隔几步CG再进行一次最陡下降

步骤，CG的效率会更高，这个间隔步数由 nstcgsteep ↪ 127 设定。简正模式分析之前需要进

行精度非常高的能量最小化，为此应该使用双精度版本的GROMACS。

l\-bfgs

用于能量最小化的准牛顿算法，基于低内存需求的Broyden\-Fletcher\-Goldfarb\-Shanno方法。

在实践中，这种方法似乎比共轭梯度法收敛得更快，但由于必要的校正步骤，此方法（还）未

并行化。

nm

对 tpr ↪ 619 文件中的结构进行简正模式分析。应该使用双精度版本的GROMACS。

tpi

测试粒子插入。拓扑中的最后一个分子是测试粒子。必须为mdrun \-rerun提供一条轨迹。

这条轨迹中不能包含待插入的分子。程序会对每帧轨迹进行 nsteps ↪ 125 次插入操作，插入

时分子的位置和取向都是随机的。如果 nstlist ↪ 128 大于 1 ，会在围绕同一随机位置半径

为 rtpi ↪ 127 的球体内进行 nstlist ↪ 128 次插入，并使用相同的配对列表。由于构造配对列表

很耗时，因此可以使用相同的列表执行几次额外的插入操作，这对计算速度几乎没有影响。随

机种子由 ld\-seed ↪ 126 设定。用于Boltzmann加权的温度由 ref\-t ↪ 137 设定，它应该与原始

轨迹的模拟温度相同。TPI正确地考虑了色散校正。所有相关的量都会写入由mdrun \-tpi

指定的文件中。插入能量的分布写入由mdrun \-tpid指定的文件中。不会生成轨迹或能量文

件。并行TPI与单节点TPI的结果完全相同。对于带电分子，使用精细网格的PME最准确，

也最有效，因为对每一帧轨迹只需要计算一次系统的势能。

tpic

测试粒子插入到预定义的空腔位置。过程与 integrator=tpi ↪ 124 相同，不同之处在于需要从

轨迹中读取一个额外的坐标作为插入位置。待插入的分子的中心应位于0,0,0。GROMACS不

会自动处理这一点，因为对于不同的情况，采用不同的居中方式可能更好。另外， rtpi ↪ 127

设置该位置周围的球体的半径。对每帧轨迹只进行一次邻区搜索，不使用 nstlist ↪ 128 。并

行 integrator=tpic ↪ 125 与单节点 integrator=tpic ↪ 125 的结果完全相同。

mimic

启用MiMiC QM/MM耦合以运行混合分子动力学。请记住，需要启动使用MiMiC编译的

CPMD。在此模式下，会忽略所有涉及积分的选项（温度耦合，压力耦合，时间步长和模拟步

数），因为积分由CPMD进行。与力的计算相关的选项（截断值，PME参数等）作用正常。

定义QM原子的原子选区由 QMMM\-grps ↪ 162 设定

tinit

\(0\) \[ps\]运行的起始时间（只对基于时间的积分方法有意义）

dt

\(0\.001\) \[ps\]积分的时间步长（只对基于时间的积分方法有意义）

nsteps

\(0\)积分或能量最小化的最大步数，\-1意味着不限制步数

init\-step

\(0\)起始步。运行时第i步对应的时刻为t = tinit ↪ 125 \+ dt ↪ 125 \* \( init\-step ↪ 125 \+ i\)。自由能

计算中的lambda为lambda = init\-lambda ↪ 154 \+ delta\-lambda ↪ 154 \* \( init\-step ↪ 125 \+ i\)。此

外，非平衡MD的参数也可以与步数有关。因此，为了准确地重新启动或重做部分模拟，可能需

要将 init\-step ↪ 125 设置为重启帧的步数。 gmx convert\-tpr ↪ 203 可以自动执行此操作。

simulation\-part

\(0\)模拟可以包含多个部分，每一部分都具有一个编号。此选项指定模拟部分的编号，有助于追踪

逻辑上相同的模拟部分。此选项通常只用于处理文件丢失的崩溃模拟。

mts

no

每个积分步都计算所有的力\.

yes

使用多重时间步长积分器计算某些力，由 mts\-level2\-forces 指定,每 mts\-level2\-factor

积分步进行一次。所有其他力会在每一步进行计算。MTS目前只支持 integrator=md\.

mts\-levels

\(2\)多重时间步长方案所用的级别数\.目前只支持2\.

mts\-level2\-forces

\(longrange\-nonbonded\)一个或多个力计算组的列表,组中力只会每 mts\-level2\-factor 步计算一

次\.支持的项目为:longrange\-nonbonded,nonbonded,pair,dihedral,angle,pull和awh\.

使用pair,会选择列出的成对力\(如1\-4\)\.使用 dihedral会选择所有的二面角,包括cmap\.所

有其他力,包括所有的限制,会在每一步进行计算并积分\.如果静电和/或LJ相互作用使用PME

或Ewald方法,这里的longrange\-nonbonded不能省略\.

mts\-level2\-factor

\(2\) \[步\]多重时间步长方案中,计算级别 2 的力时,间隔的步数\.

comm\-mode

Linear

移除质心平动速度

Angular

移除质心的平动和转动速度

Linear\-acceleration\-correction

移除质心的平动速度。假定加速度在 nstcomm ↪ 126 步中是线性的，并以此对质心位置进行校

正。如果在 nstcomm ↪ 126 步中质心的预期加速度几乎不变，此选项很有用。例如，当使用绝对

参考牵引一个组时，可能就会发生这种情况。

None

不限制质心运动

nstcomm

\(100\) \[步\]移除质心运动的频率

comm\-grps

需要移除质心运动的组，默认为整个系统

### 5\.4 Langevin 动力学

bd\-fric

\(0\) \[amu ps\-1\]布朗动力学摩擦系数。当 bd\-fric ↪ 126 为 0 时，每个粒子的摩擦系数为其质量

与 tau\-t ↪ 137 的比值。

ld\-seed

\(\-1\) \[整数\]用于初始化热噪声的随机生成器，用于随机和布朗动力学。如果 ld\-seed ↪ 126 设置

为\-1，会使用伪随机种子。当在多个处理器上运行BD或SD时，每个处理器使用的种子等

于 ld\-seed ↪ 126 加上处理器的编号。

### 5\.5 能量最小化

emtol

\(10\.0\) \[kJ mol\-1nm\-1\]当最大的力小于此值时，最小化收敛

emstep

\(0\.01\) \[nm\]初始步长大小

nstcgsteep

\(1000\) \[步\]进行共轭梯度能量最小化时，执行 1 步最速下降的频率。

nbfgscorr

\(10\) L\-BFGS最小化的校正步数。数值越高（至少理论上）越精确，但速度越慢。

### 5\.6 壳层分子动力学

##### 当系统中存在壳层或柔性约束时，会在每个时间步对壳层的位置和柔性约束的长度进行优化，直到壳层

和约束受力的RMS值小于 emtol ↪ 127 ，或者达到最大迭代次数 niter ↪ 127 。当最大的力小于 emtol ↪ 127  
时，最小化会收敛。对于壳层MD，此值最大为1\.0。

niter

\(20\)优化壳层位置和柔性约束的最大迭代次数。

fcstep

\(0\) \[ps^2 \]优化柔性约束的步长。应设置为mu/\(d2V/dq2\)，其中mu为柔性约束中两个粒子的约化

质量，d2V/dq2为势能在约束方向上的二阶导数。希望这个数字对不同的柔性约束不要相差太大，

因为迭代次数进而运行时间对fcstep非常敏感。多试几个值\!

### 5\.7 测试粒子插入

rtpi

\(0\.05\) \[nm\]测试粒子的插入半径，见积分方法 integrator=tpi ↪ 124 和 integrator=tpic ↪ 125

### 5\.8 输出控制

nstxout

\(0\) \[步\]将坐标写入输出轨迹文件（ trr ↪ 619 ）的间隔步数，最后一步的坐标始终会写入

nstvout

\(0\) \[步\]将速度写入输出轨迹文件（ trr ↪ 619 ）的间隔步数，最后一步的速度始终会写入,除非此选项

为0,因为那意味着速度不会写入轨迹文件中\.

nstfout

\(0\) \[步\]将力写入输出轨迹文件（ trr ↪ 619 ）的间隔步数，最后一步的力始终会写入,除非此选项为0,

因为那意味着力不会写入轨迹文件中\.

nstlog

\(1000\) \[步\]将能量写入日志文件的间隔步数，最后一步的能量始终会写入\.

nstcalcenergy

\(100\) \[步\]两次能量计算之间的间隔步数， 0 表示从不计算。此选项仅与动力学有关。会影响并行

模拟的性能，因为计算能量需要在所有进程之间进行全局通信，在高度并行化的情况下，这可能会

成为计算速度的瓶颈。

nstenergy

\(1000\) \[步\]将能量写入能量文件的间隔步数，最后一步的能量总会写入。此选项的值应该

为 nstcalcenergy ↪ 128 的倍数。注意，对MD步数与 nstcalcenergy ↪ 128 同余的所有步，会将精

确的能量总和及其波动写入能量文件中，因此当 nstenergy ↪ 128 > 1时， gmx energy ↪ 237 仍然可以

给出精确的能量平均值及其波动。

nstxout\-compressed

\(0\) \[步\]使用有损压缩（ xtc ↪ 621 ）文件输出位置坐标的间隔步数\.设置为 0 则不会写出压缩后的坐

标\.

compressed\-x\-precision

\(1000\) \[实数\]输出压缩轨迹文件所用的精度， 1000 代表千分之一，小数点后三位精度

compressed\-x\-grps

写入压缩轨迹文件的原子组，默认为整个系统（如果 nstxout\-compressed ↪ 128 > 0）

energygrps

将对应原子组的短程和非键势能写入能量文件（GPU不支持）

### 5\.9 邻区搜索

cutoff\-scheme

Verlet

生成带有缓冲的配对列表。缓冲区大小会根据 verlet\-buffer\-tolerance ↪ 129 自动设置，除

非将其设置为\-1，在这种情况下会使用 rlist ↪ 130 作为缓冲区大小。

2019:此选项在 rvdw ↪ 133 等于 rcoulomb ↪ 132 处存在明显，精确的截断，除非使用PME或

Ewald，在这种情况下允许 rcoulomb ↪ 132 > rvdw ↪ 133 。目前仅支持截断，反应场，PME或

Ewald静电和普通LJ。 gmx mdrun ↪ 276 的一些功能尚不支持 cutoff\-scheme=Verlet ↪ 128 方

案，但 gmx grompp ↪ 252 会对此进行检查。只有 cutoff\-scheme=Verlet ↪ 128 支持原生GPU加

速。使用GPU加速的PME或单独的PME进程时， gmx mdrun ↪ 276 会通过缩放 rcoulomb ↪ 132

和格点间距来自动调整CPU/GPU负载均衡。可以使用mdrun \-notunepme关闭此功能。当

系统中不含水分子，或者 cutoff\-scheme=group ↪ 128 使用配对列表缓冲来维持能量守恒时，

cutoff\-scheme=Verlet ↪ 128 会比 cutoff\-scheme=group ↪ 128 更快。

group

为原子组生成配对列表。这些组对应于拓扑中的电荷组。不再支持此选项\.

2019:在4\.6版之前，这是唯一的截断处理方案，自 5\.1 版起已废弃。配对列表没有明确的缓

冲。这样计算水的受力时效率很高，但只有明确地加入缓冲时能量才能守恒。

nstlist

\(10\)\[步\]

>0

更新邻区列表的频率。如果该值为 0 ，邻区列表只生成一次。

若设置了动力学和 verlet\-buffer\-tolerance ↪ 129 ， nstlist ↪ 128 实际上是最小值， gmx

mdrun ↪ 276 可能会增大它的值，除非将其设置为 1 。对GPU上的并行模拟和/或非键力

计算，取 20 或 40 通常能得到最佳性能。在能量最小化情况下，不使用该参数，因为至少有

一个原子的移动距离超过原子对列表缓冲区大小的一半时，原子对列表才会更新。

2019:对能量最小化，当 nstlist ↪ 128 大于 0 时，每次计算能量都会更新配对列表。

使用 cutoff\-scheme=group ↪ 128 和非精确的截断， nstlist ↪ 128 会影响模拟的准确性，不能

随意选择。

0

邻区列表仅构建一次，且不再更新。这主要用于真空中的模拟，在这种情况下所有粒子彼此

间都存在相互作用。 2023 版暂时不支持真空模拟\.

<0

未使用。

ns\-type 2019 版选项

grid

在盒子中生成格点，每 nstlist ↪ 128 步构建一次新的邻区列表，只有这时才检查处于相邻格

点单元格中的原子。对大的系统，格点搜索比简单搜索快得多。

simple

每 nstlist ↪ 128 步 构 建 新 的 邻 区 列 表 时， 检 查 盒 子 中 的 每 个 原 子 （仅 用

于 cutoff\-scheme=group ↪ 128 截断方案）。

pbc

xyz

在所有方向上使用周期性边界条件。

no

不使用周期性边界条件，忽略盒子。要进行无截断的模拟，可将所有截断以及 nstlist ↪ 128

设置为 0 。在单个 MPI进程上，不使用截断时，将 nstlist ↪ 128 设置为零，并使

用 ns\-type=simple ↪ 129 可获得最佳性能。

xy

只在x和y方向上使用周期性边界条件。仅适用于 ns\-type=grid ↪ 129 ，并可与 walls ↪ 142 结合

使用。没有墙或只有一面墙时，系统在z方向是无限延伸的。因此不能使用压力耦合或Ewald

求和方法。当使用两面墙时没有这些缺点。

periodic\-molecules

no

分子是有限的，可以使用快速的分子PBC

yes

用于含有通过周期性边界条件与自身耦合的分子系统，需要较慢的PBC算法，并且输出中的

分子没有进行完整化处理

verlet\-buffer\-tolerance

\(0\.005\) \[kJ mol\-1ps\-1\]

只适用于进行动力学模拟\. 对 2019 版,只适用于 cutoff\-scheme=Verlet ↪ 128 截断方案。此选

项设置由Verlet缓冲引起的每个粒子配对相互作用的最大允许误差，间接地设置了 rlist ↪ 130 。

由于 nstlist ↪ 128 和Verlet缓冲大小都是固定的（出于性能原因），不在配对列表中的粒子对

在 nstlist ↪ 128 \-1步内偶尔能够进入截断距离内。这会使能量发生非常小的跳跃。在等温系综

中，对于给定的截断和 rlist ↪ 130 可以估算出这些非常小的能量跳跃。估算时假定粒子分布均

匀，因此对多相系统的误差可能会略偏低。（详细信息见参考手册↪ 469 ）。对于更长的配对列表寿

命（ nstlist ↪ 128 \-1）\* dt ↪ 125 ，会高估缓冲，因为忽略了粒子之间的相互作用。再加上误差互相

抵消，总能量的实际漂移幅度通常要小一个到两个数量级。注意，与基于粒子对的简单列表相比，

GROMACS的配对列表设置可以将漂移降低为原来的1/10，生成缓冲大小时考虑了这一点。不使

用动力学（能量最小化等）时，缓冲为截断的5%。对NVE模拟，会使用初始温度，除非该温度

为零，在这种情况下会使用10%的缓冲。对NVE模拟通常需要降低容差，以便在纳秒时间尺度

上达到适当的能量守恒。要覆盖自动缓冲设置，可使用 verlet\-buffer\-tolerance ↪ 129 =\-1，并手

动设置 rlist ↪ 130 。

rlist

\(1\) \[nm\]短程邻区列表的截断距离。

对于动力学任务，默认由 verlet\-buffer\-tolerance 选项设置， rlist 的值会被忽略。对于非动

力学任务，默认设置为最大截断外加5%缓冲区，但测试粒子插入除外\.对于测试粒子插入会自动

精确地管理缓冲区。对于不可能自动设置的NVE模拟，建议的程序是,使用具有预期温度的NVT

设置运行gmx grompp，并将所得 rlist 的值复制到NVE设置中。

2019:使用 cutoff\-scheme=Verlet ↪ 128 截断方案时，默认由 verlet\-buffer\-tolerance ↪ 129 选项

设置，忽略 rlist ↪ 130 的值。

### 5\.10 静电

coulombtype

Cut\-off

简单截断，配对列表半径为 rlist ↪ 130 ，库仑截断为 rcoulomb ↪ 132 ，且 rlist ↪ 130 >=

rcoulomb ↪ 132 。

Ewald

经 典 的 Ewald 求 和 方 法。 实 空 间 截 断 rcoulomb ↪ 132 应 等 于 rlist ↪ 130 。 例

如， 使 用 rlist ↪ 130 =0\.9， rcoulomb ↪ 132 =0\.9。 倒 易 空 间 使 用 的 波 矢 的 最 大 振 幅

由 fourierspacing ↪ 134 控制。直接/倒易空间的相对精确度由 ewald\-rtol ↪ 135 控制。

注意：Ewald算法的复杂度为O\(N3/2\)，因此对于大的系统非常慢。包含这个算法主要用于参

考，在大多数情况下，PME方法都表现得更好。

PME

快速平滑粒子网格Ewald（SPME）静电方法。直接空间类似于Ewald求和方法，而倒易部

分使用FFT进行计算。格点大小由 fourierspacing ↪ 134 控制，插值的阶数由 pme\-order ↪ 135

控制。使用格点间距为0\.1 nm的三次插值时，静电力的计算精度为2\-3\*10\-4。由于VDW截

断的误差大于此值，你可以尝试使用0\.15 nm的格点间距。当并行运行时，插值的并行性能

优于FFT，因此可以尝试减小格点大小，同时增加插值。

P3M\-AD

粒子\-粒子\-网格算法，具有长程静电相互作用的解析导数。方法和代码与SPME完全相同，

只是影响函数针对格点进行了优化。这使得精度略有提高。

Reaction\-Field

反应场静电方法，库仑截断为 rcoulomb ↪ 132 ，且 rlist ↪ 130 >= rvdw ↪ 133 。超出截断区域的介

电常数为 epsilon\-rf ↪ 132 。设置 epsilon\-rf ↪ 132 =0时，介电常数无穷大。

Generalized\-Reaction\-Field 2019 版

广义反应场方法，库仑截断为 rcoulomb ↪ 132 ，且 rlist ↪ 130 >= rcoulomb ↪ 132 。超出截断区域

的介电常数为 epsilon\-rf ↪ 132 。离子强度根据带电（即非零电荷）电荷组的数目来计算。这

种势的温度通过 ref\-t ↪ 137 设定。

Reaction\-Field\-zero 2019 版

在GROMACS中，使用 cutoff\-scheme=group ↪ 128 时，常规的反应场静电方法能量守恒性

不好。使用 coulombtype=Reaction\-Field\-zero ↪ 131 可以解决这个问题，这时会将超出截断

的势能设置为零。只适用于介电常数无穷大的情况（ epsilon\-rf ↪ 132 =0），因为只有这样力

在截断处才会消失。 rlist ↪ 130 应比 rcoulomb ↪ 132 大0\.1到0\.3 nm，以适应电荷组的大小，

以及两次邻区列表更新之间的扩散。这一点，以及使用查表代替解析函数的作法，使得零反

应场的计算慢于常规反应场。

Shift 2019 版

类 似 于 vdwtype ↪ 132 的 vdwtype=Shift ↪ 132 。 你 可 能 希 望 使

用 coulombtype=Reaction\-Field\-zero ↪ 131 ，它具有类似的势能形状，但具有物理意

义，并且含有排除校正项，计算的能量更好。

Encad\-Shift 2019 版

库仑势在整个范围内降低，使用Encad模拟包中的定义。

Switch 2019 版

类似于 vdwtype ↪ 132 的 vdwtype=Switch ↪ 133 。切换库仑势可导致严重的假象，建议使

用 coulombtype=Reaction\-Field\-zero ↪ 131 代替。

User

2023 版目前不支持\.

gmx mdrun ↪ 276 需要读取文件table\.xvg，其中包含用户定义的势能函数，包括排斥，色散

和库仑相互作用。当存在配对相互作用时， gmx mdrun ↪ 276 还需要读取用于配对相互作用的

文件tablep\.xvg。当非键和配对需要使用相同的相互作用时，用户可以为两个表格文件指

定相同的文件名。这些文件应包含 7 列：x 值，f\(x\)，\-f'\(x\)，g\(x\)，\-g'\(x\)，h\(x\)，

\-h'\(x\)，其中f\(x\)为库仑函数，g\(x\)为色散函数，h\(x\)为排斥函数。当 vdwtype ↪ 132 未

设置为User时，会忽略g，\-g'，h和\-h'的值。对非键相互作用，x的值应该从 0 到

最大截止距离\+ table\-extension ↪ 134 ，并且间距应均匀。对于配对相互作用，会使用文件

中的表格长度。对混合精度的GROMACS，非用户自定义表格的最佳间距为 0\.002 nm，对

双精度则为0\.0005 nm。x = 0处的函数值并不重要。更多信息见手册。

PME\-Switch

2023 版目前不支持\.

PME与直接空间部分切换函数的组合（见上文）。 rcoulomb ↪ 132 可以小于 rlist ↪ 130 。主要

用于等能量模拟（注意，PME与 cutoff\-scheme=Verlet ↪ 128 一起使用效率会更高）。

PME\-User

2023 版目前不支持\.

PME与用户表格的组合（见上文）。 rcoulomb ↪ 132 可以小于 rlist ↪ 130 。 gmx mdrun ↪ 276 会从

用户表格中扣除PME网格的贡献。由于这个扣除，用户表格应包含大约 10 位小数。

PME\-User\-Switch

2023 版目前不支持\.

PME\-User和切换函数的组合（见上文）。对最终的粒子\-粒子相互作用使用切换函数，即对用

户提供的函数和PME网格校正部分都使用切换函数。

coulomb\-modifier

Potential\-shift\-Verlet 2019 版

使用Potential\-shift 与Verlet截断方案，因为它（几乎）不增加计算量；使用None与

组截断方案。

Potential\-shift

对库仑势进行固定的移位，使其在截断处为零。这样势能就等于力的积分。注意，这不会影

响力或采样。

None

使用未经修改的库仑势。当将能量与其他软件所得的值进行对比时,可能会用到此选项\.

2019:与组截断方案一起使用时，这意味着没有使用精确的截断，会计算配对列表中所有配对

之间的能量和力。

rcoulomb\-switch

\(0\) \[nm\]开始切换库仑势的位置，只适用于力或势能使用切换的情况。

rcoulomb

\(1\) \[nm\]库仑截断距离。注意，使用PME时， gmx mdrun ↪ 276 中的PME调整策略可能会导致此

值以及PME格点间距增加。

epsilon\-r

\(1\)相对介电常数。 0 意味着无穷大。

epsilon\-rf

\(0\)反应场的相对介电常数。仅用于反应场静电方法。 0 意味着无穷大。

### 5\.11 范德华作用

vdwtype

Cut\-off

简单截断，配对列表半径为 rlist ↪ 130 ，VdW截断为 rvdw ↪ 133 ，且 rlist ↪ 130 >= rvdw ↪ 133 。

PME

使用快速平滑粒子网格Ewald（SPME）方法计算VdW相互作用。与静电类似，格点大小

由 fourierspacing ↪ 134 控制，插值阶数由 pme\-order ↪ 135 控制。直接/倒易空间的相对精确

度由 ewald\-rtol\-lj ↪ 135 控制，倒易子程序使用的特定组合规则由 lj\-pme\-comb\-rule ↪ 135 设定。

Shift

此 功 能 已 废 弃， 不 推 荐 使 用， 可 替 换 为 vdwtype=Cut\-off ↪ 132

和 vdw\-modifier=Force\-switch ↪ 133 。LJ（不包括 Buckingham）势能在整个范围内都

有所降低，相应的力在 rvdw\-switch ↪ 133 和 rvdw ↪ 133 之间平滑地衰减到零。

2019:邻区搜索截断 rlist ↪ 130 应比 rvdw ↪ 133 大0\.1至0\.3 nm，以适应电荷组的大小，以及

两次邻区列表更新之间的扩散。

Switch

此 功 能 已 废 弃， 不 推 荐 使 用， 可 以 替 换 为 vdwtype=Cut\-off ↪ 132

和 vdw\-modifier=Potential\-switch ↪ 133 。LJ（不包括Buckingham）势在 rvdw\-switch ↪ 133

之内是正常的，之后逐渐降低，并在 rvdw ↪ 133 处达到零。势能和力函数都是连续平滑的，但

要注意所有的切换函数都会导致力的突起（增高，因为我们切换了势能）。

2019:邻区搜索截断 rlist ↪ 130 应比 rvdw ↪ 133 大0\.1至0\.3 nm，以适应电荷组的大小，以及

两次邻区列表更新之间的扩散。

Encad\-Shift 2019 版

LJ（不包括Buckingham）势能在整个范围内降低，使用Encad模拟包中的定义。

User

2023 版目前不支持\.

参见 coulombtype ↪ 130 的user选项。零点处的函数值并不重要。如果要使用LJ校正，请确

保 rvdw ↪ 133 对应于用户定义函数的截断值。若 coulombtype ↪ 130 未设置为 User，会忽略 f

和\-f'列的值。

vdw\-modifier

Potential\-shift\-Verlet 2019 版

使用Potential\-shift 与Verlet截断方案，因为它（几乎）不增加计算量；使用None与

组截断方案。

Potential\-shift

将范德华势偏移一个常数，使其在截断处为零。这样势能就等于力的积分。注意，这不会影

响力或采样。

None

使用未经修改的范德华势。当将能量与其他软件所得的值进行对比时,可能会用到此选项\.

2019:与组截断方案一起使用时，这意味着没有使用精确的截断，会计算配对列表中所有配对

之间的能量和力。

Force\-switch

在 rvdw\-switch ↪ 133 和 rvdw ↪ 133 之间平滑地将力切换为零。这会在整个范围内偏移势能，并

在截断处将其切换为零。请注意，这种方法比普通截断方法更耗时，并且不要求能量守恒，因

为Potential\-shift可以保证能量守恒。

Potential\-switch

在 rvdw\-switch ↪ 133 和 rvdw ↪ 133 之间平滑地将势能切换为零。注意，这会导致切换区域中的

力出现很大的虚假值，并且计算也更耗时。只有当你使用的力场要求时，才应使用此选项。

rvdw\-switch

\(0\) \[nm\]从何处开始切换LJ力或势能，只适用于对力或势能使用切换的情况。

rvdw

\(1\) \[nm\] LJ或Buckingham势的截断距离

DispCorr

no

不使用任何校正

EnerPres

对能量和压力进行长程色散校正

Ener

只对能量进行长程色散校正

### 5\.12 表格

table\-extension

\(1\) \[nm\]非键势能查询表格超出最大截断距离后的扩展长度。

对于实际的非键相互作用，表格永远不会超过截止值。但是，对于1\-4相互作用可能需要更长的表

格，因为总会将其列表,无论是否使用表格处理非键相互作用。

2019:该值应足够大，以考虑电荷组的大小以及两次邻区列表更新之间的扩散。不使用自定义势

能时，对1\-4相互作用查询表会使用相同的表格长度，这些相互作用总是以表格给出，与非键

相互作用是否使用表格无关。 table\-extension ↪ 134 的值决不可能影响 rlist ↪ 130 ， rcoulomb ↪ 132

或 rvdw ↪ 133 的值。

energygrp\-table

2023 版目前不支持\.

当静电和/或VdW使用用户表格时，可以在这里列出能量组之间的配对，这些成对的能量组

可以使用单独的用户表格。两个能量组的名称会追加到表格的文件名称中，追加时按照它们

在 energygrps ↪ 128 中定义的顺序，彼此间以下划线隔开。例如，如果energygrps = Na Cl Sol，

并且energygrp\-table = Na Na Na Cl，除常规的table\.xvg 外， gmx mdrun ↪ 276 还需要读取

table\_Na\_Na\.xvg和table\_Na\_Cl\.xvg。table\.xvg会用于所有其他配对能量组。

### 5\.13 Ewald

fourierspacing

\(0\.12\) \[nm\]对于普通Ewald方法，盒子尺寸和间距的比值决定了在每个（带符号）方向上使用的

波矢数目的下限。对于PME和P3M，该比值决定了沿每个轴使用的傅里叶空间格点数的下限。

在所有情况下，每个方向上的格点数目都可以通过非零的 fourier\-nx ↪ 134 等重新设置。为优化粒

子\-粒子相互作用计算以及PME网格计算之间的相对负载，了解下面的事实可能会有帮助：当库

仑截断和PME格点间距按相同因子缩放时，静电计算的精度几乎保持不变。注意， gmx mdrun ↪ 276

中的PME调整策略可能会缩放此间距以及 rcoulomb ↪ 132 。

fourier\-nx

fourier\-ny

fourier\-nz

\(0\)使用Ewald方法时，倒易空间中波矢的最大幅度。使用PME或P3M时对应格点的大小。

这些值会覆盖每个方向的 fourierspacing ↪ 134 设置。选择的值最好为 2 ， 3 ， 5 和 7 的幂。避免

使用大的素数。注意， gmx mdrun ↪ 276 中的PME调整策略可能会减小这些格点大小，同时缩

放 rcoulomb ↪ 132 。

pme\-order

\(4\) The number of grid points along a dimension to which a charge is mapped\. The actual order of

the PME interpolation is one less, e\.g\. the default of 4 gives cubic interpolation\. Supported values

are 3 to 12 \(max 8 for P3M\-AD\)\. When running in parallel, it can be worth to switch to 5 and

simultaneously increase the grid spacing\. Note that on the CPU only values 4 and 5 have SIMD

acceleration and GPUs only support the value 4\.

电荷映射到某一维度上时,映射沿这一维度的网格点数。PME插值的实际阶数要比此值小一，例

如默认值 4 对应三次立方插值。支持值为 3 至 12 （对P3M\-AD最大值为 8 ）。并行运行时，可能

值得将此值换为 5 ，同时增加网格间距。需要注意的是，在CPU上，只有 4 和 5 可以进行SIMD

加速，而GPU只支持 4 。

2019: PME插值的阶数。 4 对应于三次插值。并行运行时，可以尝试使用6/8/10，同时减小格点

尺寸。

ewald\-rtol

\(10\-5\) Ewald移位的直接空间势能在 rcoulomb ↪ 132 处的相对强度由 ewald\-rtol ↪ 135 给出。减少此

值会得到更精确的直接空间加和，但倒易空间加和时需要更多的波矢。

ewald\-rtol\-lj

\(10\-3\)使用PME计算VdW相互作用时， ewald\-rtol\-lj ↪ 135 用于控制 rvdw ↪ 133 处色散势的相对

强度，与 ewald\-rtol ↪ 135 控制静电势的方式类似。

lj\-pme\-comb\-rule

\(Geometric\) LJ\-PME倒易部分VdW参数的组合规则。几何规则比Lorentz\-Berthelot规则快得

多，因此通常建议优先选择几何规则，即使力场的其余部分使用了Lorentz\-Berthelot规则。

Geometric

使用几何组合规则

Lorentz\-Berthelot

使用Lorentz\-Berthelot组合规则

ewald\-geometry

3d

在所有三个维度进行Ewald求和。

3dc

倒易部分的加和仍然在3D中进行，但对z 维度上的力和势能进行校正以得到伪2D求和。

如果系统在x\-y平面具有板块几何结构，你可以尝试增加盒子在z 方向的长度（盒子的长

度通常取为板块高度的 3 倍）并使用此选项。

epsilon\-surface

\(0\)控制3D Ewald求和的偶极校正。默认值为零，表示不进行校正。将此值设置为无限系统周围

### 5\.14 温度耦合

ensemble\-temperature\-setting

auto

使用此设置后，gmx grompp会决定接下来的三个设置哪个可用，并从中选择合适的一个。当

所有原子都耦合到温度相同的温度热浴中时，会选择恒定的系综温度，其值来自温度热浴。

constant

体系具有恒定的系综温度,其值来自 ensemble\-temperature \.某些采样算法,如AWH,需要

恒定的系综温度\.

variable

由于模拟退火或模拟回火，体系的系综温度是可变的。体系的系综温度会在模拟过程中动态

设置。

not\-available

体系没有系综温度\.

ensemble\-temperature

\(\-1\) \[K\]

体系的系综温度。该输入值只有在使用ensemble\-temperature\-setting=constant时才能用到。

默认情况下，系综温度来自热浴温度（如果使用热浴的话）。

tcoupl

no

不使用温度耦合。

berendsen

通过Berendsen恒温器耦合到温度为 ref\-t ↪ 137 的热浴，时间常数为 tau\-t ↪ 137 。可以单独耦

合多个组，这些组在 tc\-grps ↪ 137 字段中指定，彼此间以空格分开。

这是一个只具有历史意义的恒温器，重现以前的模拟时会用到，但我们强烈建议不要将其用

于新的成品运行。详情请查阅手册。

nose\-hoover

使用Nose\-Hoover扩展系综进行温度耦合。参考温度与耦合组的设定方法同上，但在这种情

况下 tau\-t ↪ 137 控制的是平衡时温度的波动周期，与弛豫时间略有不同。对NVT模拟，能量

的守恒量会写入能量和日志文件。

andersen

在每个时间步将一部分粒子的速度随机化，以此进行温度耦合。参考温度和耦合组的设定方

法同上。 tau\-t ↪ 137 为每个分子两次随机化之间的平均时间间隔。此方法在一定程度上会抑制

粒子的动力学，但很少出现或没有遍历性问题。目前只能用于速度Verlet，且不能使用约束。

andersen\-massive

不频繁地选择时间步，将所有粒子的速度随机化，以此进行温度耦合。参考温度和耦合组的

设定方法同上。 tau\-t ↪ 137 是所有分子两次随机化之间的时间间隔。此方法在一定程度上会抑

制粒子的动力学，但很少出现或没有遍历性问题。目前只能用于速度Verlet方法。

v\-rescale

使用带有随机项的速度重新缩放方法进行温度耦合（JCP 126, 014101）。此恒温器类似于

Berendsen耦合，使用相同的 tau\-t ↪ 137 进行缩放，但随机项确保了能够生成适当的正则系

综。随机种子由 ld\-seed ↪ 126 设定。即使 tau\-t ↪ 137 =0\.，此恒温器也能正常工作。对NVT模

拟，能量的守恒量会写入能量和日志文件。

nsttcouple

\(\-1\)温度耦合的频率。默认值\-1将 nsttcouple 设置为100,或更少以进行精确的积分（一阶耦合

为每tau 5步，二阶耦合为每tau 20步）。需要注意的是，默认值偏大是为了减少获得动能所需的

额外计算和通信开销。对速度Verlet积分方法 nsttcouple ↪ 137 设置为 1 。

2019:默认值\-1 表示 nsttcouple ↪ 137 等于 nstlist ↪ 128 ，除非 nstlist ↪ 128 <=0，这种情况下会

使用 10 。

nh\-chain\-length

\(10\)速度Verlet积分方法中链式Nose\-Hoover恒温器的数目，蛙跳式积分方法 integrator=md ↪ 124

只 支 持 1 。 默 认 情 况 下，NH 链 变 量 的 数 据 不 会 输 出 到 edr ↪ 609 文 件， 但 可 以 使

用 print\-nose\-hoover\-chain\-variables 选项启用此功能。

print\-nose\-hoover\-chain\-variables

no

不要在能量文件中存储Nose\-Hoover链变量。

yes

在能量文件中存储Nose\-Hoover链的所有位置和速度。

tc\-grps

独立地耦合到温度浴的组

tau\-t

\[ps\]耦合时间常数（ tc\-grps ↪ 137 中的每个组设置一个值），\-1 表示不使用温度耦合

ref\-t

\[K\]耦合参考温度（ tc\-grps ↪ 137 中的每个组设置一个值）

### 5\.15 压力耦合

pcoupl

no

不使用压力耦合。这意味着盒子的大小固定。

Berendsen

指数弛豫的压力耦合，时间常数为 tau\-p ↪ 138 。盒子每 nstpcouple ↪ 138 步缩放一次。

##### 此恒压器无法得到正确的热力学系综;提供此选项只是为了重现以前的运行,因此我们强烈建

##### 议不要在新的模拟中使用它\.详情见手册\.

##### 2019:有人认为这不会产生正确的热力学系综，但在模拟的起始阶段这是缩放盒子的最有效方

##### 法。

C\-rescale

指数式弛豫压力耦合,时间常数为 tau\-p ,包含一个随机项以强制体积涨落正确\. 盒子

每 nstpcouple 步缩放一次\.预平衡和成品阶段都可以使用\.

Parrinello\-Rahman

扩展系综压力耦合，盒向量服从运动方程。原子的运动方程也耦合到此方程。不会发生瞬时

缩放。与Nose\-Hoover温度耦合类似，时间常数 tau\-p ↪ 138 为平衡时压力的波动周期。如果要

在数据收集过程中施加压力缩放，这是一个好方法，但请注意，如果模拟开始时的压力与平

衡压力不同，压力可能会出现非常大的振荡。对NPT系综的精确波动很重要的模拟，或者如

果压力耦合时间非常短，这种方法可能不合适，因为GROMACS实现的某些步骤会使用前面

时间步的压力计算当前时间步的压力。

MTTK

Martyna\-Tuckerman\-Tobias\-Klein 实 现， 只 用 于 integrator=md\-vv ↪ 124

或 integrator=md\-vv\-avek ↪ 124 ，与 Parrinello\-Rahman 非常相似。与 Nose\-Hoover 温

度耦合类似，时间常数 tau\-p ↪ 138 为平衡时压力的波动周期。如果要在数据收集过程中施加

压力缩放，这可能是更好的方法，但请注意，如果模拟开始时的压力与平衡压力不同，压力

可能会出现非常大的振荡。此方法需要体系具有恒定的系综温度\.目前仅支持各向同性缩放，

并且不能使用约束。

pcoupltype

指定所用压力耦合的各向同性类型。每种类型都有一个或多个 compressibility ↪ 139 值

和 ref\-p ↪ 139 值。但 tau\-p ↪ 138 只能使用一个值。

isotropic

各向同性压力耦合，时间常数为 tau\-p ↪ 138 。 compressibility ↪ 139 和 ref\-p ↪ 139 各需要一个

值。

semiisotropic

x 和 y 方向的压力耦合各向同性，与 z 方向上的不同。对于膜模拟非常有用。

compressibility ↪ 139 和 ref\-p ↪ 139 各需要两个值，分别用于x/y和z方向。

anisotropic

同上，但需要 6 个值，分别对应xx，yy，zz，xy/yx，xz/zx和yz/zy分量。如果非对

角线压缩率设置为零，长方盒子在模拟过程中将保持为长方体。请注意，各向异性缩放可能

会导致模拟盒子的剧烈变形。

surface\-tension

表面张力耦合，用于平行于xy平面的表面。 z 方向采用正常的压力耦合，而表面张力耦合到

盒子的 x/y 方向。 ref\-p ↪ 139 的第一个值为参考表面张力乘以表面数目，单位bar nm，第二

个值是参考 z 压力，单位bar。两个 compressibility ↪ 139 的值分别为 x/y 和 z 方向的压缩

系数。 z 方向压缩系数的值应该具有一定的准确度，因为它会影响表面张力的收敛，也可以将

其设置为零，以维持盒子的高度不变。

nstpcouple

\(\-1\)压力耦合的频率。默认值\-1将 nstpcouple ↪ 138 设置为100,或更少以进行精确的积分（一阶

耦合为每tau 5步，二阶耦合为每tau 20步）。需要注意的是，默认值偏大是为了减少获得动能所

需的额外计算和通信开销。对速度Verlet积分方法 nstpcouple ↪ 138 设置为 1 。

2019:默认值\-1 表示 nstpcouple ↪ 138 等于 nstlist ↪ 128 ，除非 nstlist ↪ 128 <=0，这种情况下会

使用 10 。

tau\-p

\(1\) \[ps\]压力耦合的时间常数（所有方向使用同一个值）。

compressibility

\[bar\-1\]压缩系数（注意：现在真的以bar\-1为单位）。对于1 atm，300 K的水，压缩系数为4\.5e\-5

bar\-1。所需值的数目由 pcoupltype ↪ 138 决定。

ref\-p

\[bar\]耦合的参考压力。所需值的数目由 pcoupltype ↪ 138 决定。

refcoord\-scaling

no

不修改位置限制的参考坐标。注意，使用此选项时，维里和压力可能无法良好地定义，详细

说明见位置限制↪ 541 。

all

使用压力耦合缩放矩阵来缩放参考坐标。

com

使用压力耦合缩放矩阵缩放参考坐标的质心。每个参考坐标到质心的向量不进行缩放。只使

用一个质心，即使有多个分子存在位置限制。在计算初始构型参考坐标的质心时，不考虑周

期性边界条件。注意，使用此选项时，维里和压力可能无法良好地定义，详细说明见位置限

制↪ 541 。

### 5\.16 模拟退火

##### GROMACS中每个温度组的模拟退火可以分开控制。参考温度是一个分段线性函数，但每个组可以使用

##### 任意数目的点，并可以选择选择单一序列退火类型或周期性退火类型。实际退火是通过动态地改变参考

##### 温度来进行的，由于选择的控温算法也使用该温度，所以要记住，系统通常不会立即达到参考温度\!

annealing

每个温度组的退火类型

no

不进行模拟退火，只耦合到参考温度值。

single

退火点的单一序列。如果模拟时间长于最后一个退火点的时间，当退火序列到达最后的时间

点后，温度将耦合到最后时间点的值并保持不变。

periodic

一旦达到最后的参考时间，退火将从第一个参考点处重新开始。此过程不断重复，直至模拟

结束。

annealing\-npoints

##### 每个温度组退火参考/控制点数目的列表。对不退火的组使用 0 。此项的数目应等于温度组的数目。

annealing\-time

每个温度组退火参考/控制点的时间列表。如果使用周期性退火，使用的退火时间会是模拟时间与

最大退火时间的同余，即，如果退火时间点为 0 ， 5 ， 10 和 15 ，那么耦合将在15 ps，30 ps，45 ps

等时间点后以0 ps时的值重新启动。此项的数目应等于 annealing\-npoints ↪ 139 中给出的数字之

和。

annealing\-temp

每个温度组退火参考/控制点的温度列表。此项的数目应等于 annealing\-npoints ↪ 139 中给出的数

字之和。

### 5\.17 速度产生

gen\-vel

no

不产生速度。使用输入结构文件中的速度值。如果输入结构文件中不存在速度，则将速度设

置为零。

yes

gmx grompp ↪ 252 根据温度为 gen\-temp ↪ 140 的Maxwell分布产生，随机种子为 gen\-seed ↪ 140 。

此选项只对 integrator=md ↪ 124 有意义。

gen\-temp

\(300\) \[K\] Maxwell分布的温度

gen\-seed

\(\-1\) \[整数\]用于初始化产生随机速度的随机生成器，如果 gen\-seed ↪ 140 设置为\-1，会使用伪随机

种子。

### 5\.18 键约束

constraints

控制将拓扑中的哪些键转换为刚性的完整约束。注意，典型的刚性水模型没有键，而含有专门的

\[settles\]指令，因此不受此关键词影响。

none

不会将键转换为约束。

h\-bonds

将涉及氢原子的键转换为约束。

all\-bonds

将所有键转换为约束。

h\-angles

将所有键转换为约束，并将涉及氢原子的键角转换为键约束。

all\-angles

将所有键转换为约束，并将所有键角转换为键约束。

constraint\-algorithm

选择所有非SETTLE完整约束的求解器。

LINCS

线性约束求解器。使用区域分解时与并行版本的P\-LINCS一起使用。使用 lincs\-order ↪ 141

设置精度，同时也设置了矩阵求逆展开中使用的矩阵数目。经过矩阵求逆校正后，算法会执

行一次迭代校正以补偿因旋转导致的键伸长。这种迭代的次数可通过 lincs\-iter ↪ 141 控制。

每隔 nstlog ↪ 127 步，会将相对约束偏差的均方根输出到日志文件。如果某条键在一步中的旋

转角度超过了 lincs\-warnangle ↪ 141 设定值，会将警告输出到日志文件，同时将警告打印到

标准错误输出stderr。LINCS不能用于耦合键角约束。

SHAKE

SHAKE比LINCS稍慢且不太稳定，但能用于键角约束。相对容差由 shake\-tol ↪ 141 设置，

对“常规”MD，0\.0001是合适的值。SHAKE不支持处于不同分解区域上的原子之间的约束，

因此只有在使用所谓的更新组时才能与区域分解一起使用，这通常是指受约束的键只涉及氢

原子的情况。SHAKE不能用于能量最小化。

2019:当存在电荷组之间约束时，它不能与区域分解一起使用。

continuation

此选项以前称为unconstrained\-start。

no

对初始构型施加约束，并重置壳层。

yes

不对初始构型施加约束，也不重置壳层。对于精确的MD续算和重算很有用。

shake\-tol

\(0\.0001\) SHAKE的相对容差

lincs\-order

\(4\)约束耦合矩阵展开的最高阶数。当约束形成三角形时，对这些三角形之内的耦合会在正常的

展开之上再施加一个相同阶数的附加展开。对“常规”MD模拟，通常 4 阶就足够了，对涉及虚

拟位点并使用大时间步长的模拟或BD，需要使用 6 阶。对双精度下精确的能量最小化，可能需

要使用 8 或更高的阶数。请注意，对于单精度，由于舍入误差的放大，阶数高于 6 时通常会导致

精度降低。与区域分解一起使用时，单元格大小由 lincs\-order ↪ 141 \+1个约束张成的距离决定。

如果想进行超过此限制的缩放，可以减小 lincs\-order ↪ 141 并增加 lincs\-iter ↪ 141 ，因为当\(1\+

lincs\-iter ↪ 141 \)\* lincs\-order ↪ 141 保持不变时，精度不会下降。

lincs\-iter

\(1\) LINCS中用于校正旋转伸长的迭代次数。对于常规模拟，一次就足够了，但对于NVE模拟，

如果需要精确的能量守恒或精确的能量最小化，可能需要将其增加到 2 。请注意，对于单精度，由

于舍入误差的放大，迭代次数超过 1 时通常会导致精度降低。

lincs\-warnangle

\(30\) \[度\]在LINCS警告前键可以旋转的最大角度

morse

no

使用简谐势描述键

yes

使用Morse势描述键

### 5\.19 能量组排除

energygrp\-excl

排除所有非键相互作用的能量组对。例如：如果你有两个能量组 Protein 和 SOL，指定

energygrp\-excl = Protein Protein SOL SOL 则只会计算蛋白质和溶剂之间的非键相互作用。

对于加快mdrun \-rerun的能量计算，排除冻结组内部的相互作用，此选项特别有用。

### 5\.20 墙

nwall

\(0\)设置为 1 时，在z=0处有一面墙，设置为 2 时，在z=z\-box处也有一面墙。墙只能与 pbc ↪ 129 =xy

一起使用。当设置为 2 时，可以使用压力耦合和Ewald求和（通常最好使用半各向同性的压力耦

合，并将x/y压缩系数设置为 0 ，否则表面积会发生变化）。墙与系统的其余部分存在相互作用，

相互作用强度由可选的墙原子类型 wall\-atomtype ↪ 142 决定。会自动添加能量组wall0和wall1

（ nwall ↪ 142 =2时），以监测能量组与每面墙之间的相互作用。不会进行z方向的质心运动移除。

wall\-atomtype

每面墙的原子在力场中的原子类型名称。通过（例如）在拓扑中定义一个特殊的墙原子类型及其组

合规则，可以独立地调整每个原子类型与墙的相互作用。

wall\-type

直接的LJ势，由与墙的z 距离决定

table

用户自定义的势能，使用与墙的z距离作为索引，以类似于 energygrp\-table ↪ 134 选项的方式读

入，其中第一个名称来自“常规”能量组，第二个名称为wall0或wall1，只使用表格中的色散

和排斥列。

wall\-r\-linpot

\(\-1\) \[nm\]与墙的距离在此值以下时，势能线性连续，因此力是恒定的。将此选项设置为正值，有

助于解决平衡时某些原子超出墙的问题。如果此值<=0（<0适用于 wall\-type ↪ 142 =table），原子

超出墙时会出现致命错误。

wall\-density

\[nm\-3\] / \[nm\-2\]每面墙的原子数密度，适用于类型为9\-3和10\-4的墙

wall\-ewald\-zfac

\(3\)第三个盒向量的缩放因子，仅用于Ewald求和，最小值为 2 。Ewald求和只能与 nwall ↪ 142 =2

一起使用，并需要使用 ewald\-geometry ↪ 135 =3dc。盒子中的真空层的作用是降低周期性映像之间

的不合实际的库仑相互作用。

### 5\.21 质心牵引

##### 设置是否激活对集约变量的牵引\. 注意，在适用的情况下，牵引坐标可以超过一个（使

用 pull\-ncoords ↪ 144 设置），并相应地存在多个相关的 mdp ↪ 612 变量。诸如 pull\-coord1\-vec ↪ 147 之  
类的选项应理解为用于适用的牵引坐标。例如，第二个牵引坐标由pull\-coord2\-vec，pull\-coord2\-k  
等描述。

pull

no

无质心牵引。忽略以下所有的牵引选项（ mdp ↪ 612 文件中如果存在这类选项，会导致警告）

yes

在一个或多个组上施加质心牵引，使用一个或多个牵引坐标。

pull\-cylinder\-r

\(1\.5\) \[nm\]圆柱的半径，用于 pull\-coord1\-geometry=cylinder ↪ 145

pull\-constr\-tol

\(10\-6\)约束牵引的相对约束容差

pull\-print\-com

no

不输出任何组的质心

Yes

输出所有牵引坐标的所有组的质心

pull\-print\-ref\-value

no

不输出每个牵引坐标的参考值

yes

输出每个牵引坐标的参考值

pull\-print\-components

no

只输出每个牵引坐标的距离

yes

输出 pull\-coord1\-dim ↪ 146 选中的距离和笛卡尔分量

pull\-nstxout

\(50\)所有牵引组质心的输出频率（为 0 时从不输出）

pull\-nstfout

\(50\)所有牵引组受力的输出频率（为 0 时从不输出）

pull\-pbc\-ref\-prev\-step\-com

no

使用参考原子（ pull\-group1\-pbcatom ↪ 144 ）处理周期性边界条件。

yes

使 用 上 一 步 的 质 心 作 为 参 考 来 处 理 周 期 性 边 界 条 件。 使 用 参 考 原 子

（ pull\-group1\-pbcatom ↪ 144 ）初始化参考值，参考原子应位于组的中间。如果一个或多

个牵引组较大，使用上一步的质心可能会很有用。

pull\-xout\-average

no

输出所有牵引组的瞬时坐标。

yes

输出所有牵引组（自上次输出以来）的平均坐标。注意，一些分析工具可能需要瞬时牵引输

出。

pull\-fout\-average

no

输出所有牵引组的瞬时力。

yes

输出所有牵引组（自上次输出以来）的平均力。注意，一些分析工具可能需要瞬时牵引输出。

pull\-ncoords

\(1\)牵引坐标的数目。下面只给出坐标 1 的牵引选项，其他坐标只要简单增加坐标索引号即可。

pull\-group1\-name

牵引组的名称。在索引文件或默认组中查找，以获得所涉及的原子。

pull\-group1\-weights

可选的相对权重，与原子的质量相乘给出质心的总权重。此项的值应为 0 ，表示所有原子的相对

权重都为 1 ，或者，此项的值也可以是牵引组中的原子数。

pull\-group1\-pbcatom

\(0\)用于处理原子组内部周期性边界条件的参考原子（不影响原子组之间的pbc）。只有当牵引组

的直径超过最短盒向量长度的一半时，此选项才重要。为确定质心，将组中的所有原子置于其最接

近 pull\-group1\-pbcatom ↪ 144 的周期映像位置。此选项值为 0 表示使用最中间的一个原子（按编

号顺序），这只适用于小的原子组。 gmx grompp ↪ 252 会检查从参考原子（特别选中，或未选中）到

组中其他原子的最大距离是否过大。此参数不能与 pull\-coord1\-geometry ↪ 145 =cylinder一起

使用。此选项值为\-1时启用余弦加权，这对周期性系统中的一组分子有用，例如水的板块（参见

Engin等人的论文J\. Chem\. Phys\. B 2010）。

pull\-coord1\-type

umbrella

使用参考组与一个或多个组之间的伞形势来牵引质心。

constraint

使用参考组与一个或多个组之间的约束来牵引质心。除使用刚性约束而不是简谐势外，该设

置与umbrella选项完全相同。注意,此类型不支持与多重时间步长联合使用\.

constant\-force

使用线性势牵引质心，因此力是恒定的。此选项没有参考位置，因此不会使用参

数 pull\-coord1\-init ↪ 147 和 pull\-coord1\-rate ↪ 147 。

flat\-bottom

距离超出 pull\-coord1\-init ↪ 147 后会施加简谐势，否则不施加任何势。

flat\-bottom\-high

距离小于 pull\-coord1\-init ↪ 147 时会施加简谐势，否则不施加任何势。

external\-potential

需要由另一个模块提供外部的势能。

pull\-coord1\-potential\-provider

当 pull\-coord1\-type ↪ 145 为external\-potential时，提供势能的外部模块的名称。

pull\-coord1\-geometry

distance

沿连接两个组的向量进行牵引。可以使用 pull\-coord1\-dim ↪ 146 选择向量分量。

direction

沿 pull\-coord1\-vec ↪ 147 方向进行牵引。

direction\-periodic

与 pull\-coord1\-geometry=direction ↪ 145 相似，但不使用周期性边界条件对距离进行校正，

允许距离超过盒子长度的一半。（只有）通过使用牵引速率连续改变参考位置，将两个组推离

开的距离超过盒子长度一半时，才需要这个选项。使用这种牵引几何设置，盒子在牵引维度

不能变化（例如无压力缩放），并且维里中不包括牵引力的贡献。

direction\-relative

与 pull\-coord1\-geometry=direction ↪ 145 类似，但牵引向量从第三个牵引组的质心指向第

四个牵引组的质心。这意味着需要为 pull\-coord1\-groups ↪ 146 提供 4 个组。注意，牵引力会

在牵引向量上产生力矩，这导致定义牵引向量的两个组受到垂直于牵引向量的力。如果希望

一个牵引组在定义向量的两个组之间移动，只需要将这两个组的并集作为参考组就好了。

cylinder

用于相对于层的牵引，参考质心由参考组的一个局部圆柱形部分给出。牵引方向

为 pull\-coord1\-vec ↪ 147 。 pull\-coord1\-groups ↪ 146 设置了两个组，从其中的第一个选

择一个圆柱，圆柱的轴通过第二个组的质心，沿 pull\-coord1\-vec ↪ 147 方向，半径

为 pull\-cylinder\-r ↪ 143 。当径向距离从 0 变为 pull\-cylinder\-r ↪ 143 时，原子的权重连

续地减小到零（也会使用质量加权）。这种径向依赖性会导致两个牵引组上产生径向力。注意，

圆柱半径应小于盒子大小的一半。对于倾斜圆柱，其半径甚至应该比盒子大小的一半还小一

些，因为参考组中的原子到牵引组质心的距离同时具有径向和轴向分量。约束牵引不支持这

种牵引几何。

angle

沿由四个组定义的角进行牵引。该角度定义为两个向量之间的夹角：连接第一组质心和第二

组质心的向量，连接额第三组质心和第四组质心的向量。

angle\-axis

类似 pull\-coord1\-geometry=angle ↪ 146 ，但第二个向量由 pull\-coord1\-vec ↪ 147 给出。因此，

只需要给出定义第一个向量的两个组。

dihedral

沿由六个组定义的二面角牵引。六个组定义了三个向量：连接组 1 质心到组 2 质心的向量，

连接组 3 质心到组 4 质心的向量，连接组 5 质心到组 6 质心的向量。二面角定义为两个平面

间的夹角：由前两个向量张成的平面和由后两个向量张成的平面。

transformation

使用数学表达式变换其他牵引坐标,数学表达式由 pull\-coord1\-expression 定义\.低序号的

牵引坐标以及时间可作为该牵引坐标的变量。因此，牵引变换坐标的牵引坐标序号应高于其

变换的所有牵引坐标。

pull\-coord1\-expression

将具有较低序号的牵引坐标变换为新坐标的数学表达式。牵引坐标在方程中被视为变量，因

此pull\-coord1的值变为”x1”，pull\-coord2的值变为”x2”,以此类推。时间也可以用作变量，变

为”t”。请注意，表达式中的角坐标以弧度为单位。数学表达式使用muParser进行求值。只有

当 pull\-coord1\-geometry 设置为transformation时才会用到。

pull\-coord1\-dx

\(1e\-9\) Size of finite difference to use in numerical derivation of the pull coordinate with respect to

other pull coordinates\. The current implementation uses a simple first order finite difference method

to perform derivation so that f’\(x\) = \(f\(x\+dx\)\-f\(x\)\)/dx Only relevant if pull\-coord1\-geometry

is set totransformation\.

计算牵引坐标相对于其他牵引坐标的数值导数时,所用的有限差分的大小。目前的实现使用简单的

一阶有限差分法进行求导，因此f’\(x\) = \(f\(x\+dx\)\-f\(x\)\)/dx\.只有当 pull\-coord1\-geometry 设置

为transformation时才会用到。

pull\-coord1\-groups

与此牵引坐标作用的组的索引。所需要的组的索引数取决于牵引几何。第一个索引可以是 0 ，在这

种情况下使用 pull\-coord1\-origin ↪ 147 的绝对参考。使用绝对参考时系统不再具有平移不变性，

你应该考虑如何处理质心运动。

pull\-coord1\-dim

\(Y Y Y\) 选 择 此 牵 引 坐 标 作 用 的 维 度， 如 果 pull\-print\-components ↪ 143 =

pull\-coord1\-start=yes ↪ 147 会将这些维度写入输出文件。使用 pull\-coord1\-geometry ↪ 145 =

pull\-coord1\-geometry=distance ↪ 145 时，只有设置为Y的直角分量才会对距离有贡献。因此设

置为Y Y N只会考虑x/y平面内的距离。对于其他牵引几何， pull\-coord1\-vec ↪ 147 中所有非零

的项都应设置为Y，其他维度的值只影响输出。

pull\-coord1\-origin

\(0\.0 0\.0 0\.0\)使用绝对参考时，牵引的参考位置。

pull\-coord1\-vec

\(0\.0 0\.0 0\.0\)牵引方向。 gmx grompp ↪ 252 会归一化此向量。

pull\-coord1\-start

no

不要修改 pull\-coord1\-init ↪ 147

yes

将初始构型的质心距离加到 pull\-coord1\-init ↪ 147

pull\-coord1\-init

\(0\.0\) \[nm\]或\[度\] t=0时刻的参考距离或参考角度。

pull\-coord1\-rate

\(0\)\[nm/ps\]或\[度/ps\]参考位置或参考角度的变化速率。

pull\-coord1\-k

\(0\) \[kJ mol\-1nm\-2\]或\[kJ mol\-1nm\-1\]或\[kJ mol\-1rad\-2\]或\[kJ mol\-1rad\-1\]力常数。对于伞

形牵引，此值为简谐力常数，单位为kJ mol\-1nm\-2（或kJ mol\-1rad\-2，当用于角度时）。对

于恒力牵引，此值为线性势的力常数，因此为恒力的负值（\!），单位为kJ mol\-1nm\-1（或kJ

mol\-1rad\-1，当用于角度时）。注意，对于角度，力常数以弧度表示（而 pull\-coord1\-init ↪ 147

和 pull\-coord1\-rate ↪ 147 以度表示）。

pull\-coord1\-kB

\(pull\-k1\) \[kJ mol\-1 nm\-2\] 或 \[kJ mol\-1 nm\-1\] 或 \[kJ mol\-1 rad\-2\] 或 \[kJ mol\-1 rad\-1\]

与 pull\-coord1\-k ↪ 147 类似，但用于B状态。只有 free\-energy ↪ 153 启用时才使用此选项。这

种情况下力常数为\(1 \- lambda\) \* pull\-coord1\-k ↪ 147 \+ lambda \* pull\-coord1\-kB ↪ 147 。

### 5\.22 AWH 自适应偏置

awh

no

无偏置。

yes

使用AWH方法自适应地偏置反应坐标并估计相应的PMF。这需要体系具有恒定的系综温度\.

PMF和其他AWH数据会以 awh\-nstout ↪ 148 指定的固定间隔输出到能量文件，可以使用gmx

awh工具提取这些数据。可以通过将每个维度映射到牵引坐标索引，使用多维AWH坐标。这

种情况下，对相关的牵引坐标索引，必须使用 pull\-coord1\-type=external\-potential ↪ 145

和 pull\-coord1\-potential\-provider ↪ 145 =awh。AWH不支持direction\-periodic,以

及变换坐标依赖于时间的牵引几何。

awh\-potential

convolved

所 施 加 的 偏 置 势 为 偏 置 函 数 与 一 组 简 谐 伞 形 势 的 卷 积 （见 后 面

的 awh\-potential=umbrella ↪ 148 ）。这样可以得到光滑的势能和力。势能的分辨率由

每个伞形势的力常数指定，参见 awh1\-dim1\-force\-constant ↪ 150 。此选项不兼容使用自由能

lambda状态作为AWH反应坐标的情况\.

umbrella

使用蒙特卡洛采样方法控制简谐势的位置，以此来施加势能偏置。力常数

由 awh1\-dim1\-force\-constant ↪ 150 指定。伞的位置使用蒙特卡洛方法进行采样，

每 awh\-nstsample ↪ 148 步一次。当使用自由能lambda状态作为AWH反应坐标时,需要

此选项\.除此之外,此选项主要用于比较和测试,因为使用伞形势没有优势。

awh\-share\-multisim

no

如果启动 gmx mdrun ↪ 276 时使用了\-multidir选项，AWH不会在模拟过程中共享偏置。所

有偏置都是独立的。

yes

如 果 gmx mdrun ↪ 276 使 用 了 \-multidir 选 项， 在 模 拟 过 程 中， 对 具

有 awh1\-share\-group ↪ 150 >0 的 偏 置， 偏 置 和 PMF 估 计 值 会 与 具 有 相

同 awh1\-share\-group ↪ 150 值的偏置共享。共享时，模拟应具有相同的AWH设置，这

样才有意义。 gmx mdrun ↪ 276 会检查模拟在技术上是否适合兼容，但用户应该检查偏置共享

在物理上是否合理。

awh\-seed

\(\-1\) 对伞形势位置进行采样时，蒙特卡洛的随机种子，\-1 表示自动生成种子。只能

与 awh\-potential=umbrella ↪ 148 一起使用。

awh\-nstout

\(100000\)将AWH数据输出到能量文件的间隔步数，应该是 nstenergy ↪ 128 的倍数。

awh\-nstsample

\(10\)坐标值采样之间的间隔步数。采样是更新偏置，估计PMF和其他AWH可观测量的基础。

awh\-nsamples\-update

\(10\)用于每次AWH更新的坐标样本的数目。以步为单位的更新间隔是 awh\-nstsample ↪ 148 与此

值的乘积。

awh\-nbias

\(1\)偏置的数目，每个偏置都作用于自己的坐标上。应该为每个偏置指定以下选项，尽管下面只给

出了偏置编号为 1 的选项。通过将 1 替换为偏置索引就可以得到其他偏置索引对应的选项。

awh1\-error\-init

\(10\.0\) \[kJ mol\-1\] 相应偏置的 PMF 初始平均误差的估计值。该值与给定的扩散常

数 awh1\-dim1\-diffusion ↪ 151 一起确定了初始偏置速率。误差显然无法 提前知道。但

是，只需要 awh1\-error\-init ↪ 148 的粗略估计值。作为一般准则，在开始新的模拟时，使

用 awh1\-error\-init ↪ 148 的默认值。另一方面，如果有PMF的先验信息（例如，当提供了

PMF的初始估计时，参见 awh1\-user\-data ↪ 149 选项）， awh1\-error\-init ↪ 148 应反映这些信息。

awh1\-growth

exp\-linear

每个偏置都保留坐标样本的参考权重直方图。其大小设置了偏置函数和自由能估计值更新的幅度

（少的样本对应于大的更新，反之亦然）。因此，其增长速率设定了最大收敛速率。默认情况下存在

一个初始阶段，其过程中的直方图接近指数增长（但慢于采样率）。在随后的最终阶段，增长速率

是线性的并等于采样率（由 awh\-nstsample ↪ 148 指定）。当开始新的模拟时，偏置尚未将高的自由

能势垒平坦化，通常需要使用初始阶段提高收敛效率。

linear

与 awh1\-growth=exp\-linear ↪ 148 类 似， 但 跳 过 初 始 阶 段。 如 果 存 在 先 验知 识

（见 awh1\-error\-init ↪ 148 ） ，从而不再需要初始阶段，可以使用此选项。这也设置了

与 awh1\-target=local\-boltzmann ↪ 149 的兼容性。

awh1\-equilibrate\-histogram

no

不对直方图进行平衡。

yes

在进入初始阶段之前（参见 awh1\-growth=exp\-linear ↪ 148 ），确保采样权重的直方图足够接

近目标分布（具体而言，至少需要80%的目标区域具有小于20%的局部相对误差）。通常只

有 awh1\-share\-group ↪ 150 > 0且初始构型不能很好地代表目标分布时，才使用此选项。

awh1\-target

constant

对定义的采样区间（由\[ awh1\-dim1\-start ↪ 150 ， awh1\-dim1\-end ↪ 151 \]指定），将偏置调整为

固定（均匀）的坐标分布。

cutoff

类 似 于 awh1\-target=constant ↪ 149 ， 但 目 标 分 布 正 比 1/\(1 \+ exp\(F \-

awh1\-target=cutoff ↪ 149 \)\)，其中F为相对于估计的全局最小值的自由能。这可以将

自由能低于截断值区域中的平坦目标分布平滑地切换到自由能高于截断值区域中的

Boltzmann分布。

boltzmann

目标分布为 Boltzmann 分布，具有缩放的 beta（温度倒数）因子，缩放因子

由 awh1\-target\-beta\-scaling ↪ 149 指定。例如，值为0\.1时采样所得的坐标分布，与将

模拟温度提高为原来的 10 倍采样所得的分布相同。

local\-boltzmann

相同的目标分布，使用 awh1\-target\-beta\-scaling ↪ 149 ，但向目标分布的收敛本质上是局部

的，即偏置的变化率只取决于局部采样。这种局部收敛性质只与 awh1\-growth=linear ↪ 149 兼

容，因为对于 awh1\-growth=exp\-linear ↪ 148 ，直方图在初始阶段会进行全局重新缩放。

awh1\-target\-beta\-scaling

\(0\)对于 awh1\-target=boltzmann ↪ 149 和 awh1\-target=local\-boltzmann ↪ 149 ，指定无单位的beta

比例因子，范围为\(0,1\)。

awh1\-target\-cutoff

\(0\) \[kJ mol\-1\]对于 awh1\-target=cutoff ↪ 149 ，指定截断值，其值应该> 0。

awh1\-user\-data

no

使用默认值初始化PMF和目标分布。

yes

使用用户提供的数据初始化PMF 和目标分布。对 awh\-nbias ↪ 148 = 1， gmx mdrun ↪ 276

需要读取运行目录下的 awhinit\.xvg 文件。对于多重偏置， gmx mdrun ↪ 276 需要读取

awhinit1\.xvg，awhinit2\.xvg 等文件。可以使用 \-awh 选项更改文件名。每个输入文

件的第一个 awh1\-ndim ↪ 150 列应包含坐标值，这样每行可以定义坐标空间中的一个点。

第 awh1\-ndim ↪ 150 \+ 1列应包含每个点的PMF值\(单位kT\)。目标分布所在的列可以位于

PMF（第 awh1\-ndim ↪ 150 \+ 2列）之后，也可以与 gmx awh ↪ 188 写入的列相同。

awh1\-share\-group

positive

在模拟之间共享偏置以及PMF估计\.目前只能用于具有相同索引号偏置之间\.注意,目前不

支持在单个模拟之间共享\.偏置会在具有相同 awh1\-share\-group 值的模拟间共享。为此,使

用 awh\-share\-multisim=yes 和gmx mdrun选项\-multidir\.共享最初可能会提高收敛性，

尽管起始构型可能很关键，尤其当在许多偏置之间共享时。

2019: 在模拟内部和/或模拟之间共享偏置以及 PMF 估计。在模拟内部，具有相

同 awh1\-share\-group ↪ 150 索引的偏置之间会共享偏置（注意，当前代码不支持此选项）。

使用 awh\-share\-multisim=yes ↪ 148 以及 gmx mdrun ↪ 276 的\-multidir 选项时，会在模拟之

间共享偏置。目前，正值组的值应从 1 开始，并且对于每个后续共享偏置增加 1 。

awh1\-ndim

1. \[整数\]坐标的维数，每维映射到 1 个牵引坐标。应为每个这样的维度指定以下选项。下面只给

出了维度编号为 1 的选项。通过将 1 替换为维度索引就可以得到其他维度索引对应的选项。

awh1\-dim1\-coord\-provider

pull

pull模块为该维度提供反应坐标的模块。对于多重时间步长, AWH和pull处于相同的MTS

级别\.

2019:目前AWH只能作用于牵引坐标。

awh1\-dim1\-coord\-index

\(1\)定义该坐标维度的牵引坐标的索引。

awh1\-dim1\-force\-constant

\(0\) \[kJ mol\-1nm\-2\]或\[kJ mol\-1rad\-2\]沿该坐标维度的（非卷积）伞形势的力常数。

awh1\-dim1\-start

\(0\.0\) \[nm\]或 \[度\] 沿此维度的采样区间的起始值。允许值的范围取决于相关的牵引几

何（参见 pull\-coord1\-geometry ↪ 145 ）。对于二面角牵引几何， awh1\-dim1\-start ↪ 150 可以大

于 awh1\-dim1\-end ↪ 151 。这种情况下，区间会从\+period/2环绕到\-period/2。牵引几何为direction

时，当方向沿盒向量并且覆盖长度超过盒子的95%时，此维度是周期性的。注意，不应该在周期

性维度上施加压力耦合。

awh1\-dim1\-end

\(0\.0\) \[nm\]或\[度\]结束值，与 awh1\-dim1\-start ↪ 150 一起定义了采样区间。

awh1\-dim1\-diffusion

\(10\-5\) \[nm^2 /ps\], \[rad^2 /ps\]或\[ps\-1\]该坐标维度上扩散系数的估计值，决定初始偏置速率。只需要

粗略的估计值，除非设置为非常低的值，导致收敛缓慢，或设置为非常高的值，迫使系统远离平

衡，否则不应对结果产生严重影响。如果没有明确地指定此值，程序会给出警告。

awh1\-dim1\-cover\-diameter

\(0\.0\) \[nm\]或\[度\]在初始阶段，围绕坐标值进行单次模拟，在将该点视为已覆盖之前需要进行采样

的直径（参见 awh1\-growth=exp\-linear ↪ 148 ）。指定值> 0可以确保对于每一覆盖，在每个坐标

值上存在该直径的连续过渡。对于独立模拟而言，这很显然，但对于多个偏置共享模拟则不是这样

（ awh1\-share\-group ↪ 150 >0）。当直径为 0 时，一旦模拟对整个区间进行了采样，就会发生覆盖，

对于许多共享模拟而言，这并不能保证存在跨越自由能垒的过渡。另一方面，当直径>=采样区

间长度时，如果单次模拟独立地采样了整个区间，就会发生覆盖。

### 5\.23 强制旋转

这些 mdp ↪ 612 参数可用于强制一组原子进行旋转，例如一个蛋白质亚基。参考手册↪ 469 详细描述了可用  
于实现强制旋转的 13 种不同的势能函数。

rotation

no

不施加强制旋转。忽略所有强制旋转选项（如果 mdp ↪ 612 文件出现有关选项，会给出警告）。

yes

将 rot\-type0 ↪ 151 选项指定的旋转势施加到 rot\-group0 ↪ 151 选项指定的原子组上。

rot\-ngroups

\(1\)旋转组的数目。

rot\-group0

索引文件中的旋转组 0 的名称。

rot\-type0

\(iso\)施加到旋转组 0 的旋转势的类型。可以指定以下值：iso，iso\-pf，pm，pm\-pf，rm，rm\-pf，

rm2，rm2\-pf，flex，flex\-t，flex2 或flex2\-t。

rot\-massw0

\(no\)使用质量加权的旋转组位置。

rot\-vec0

\(1\.0 0\.0 0\.0\)旋转向量，使用前会将其归一化。

rot\-pivot0

\(0\.0 0\.0 0\.0\) \[nm\]iso，pm，rm和rm2势能的轴点。

rot\-rate0

\(0\) \[度ps\-1\]组 0 的参考旋转速率。

rot\-k0

\(0\) \[kJ mol\-1nm\-2\]组 0 的力常数。

rot\-slab\-dist0

\(1\.5\) \[nm\]柔性轴旋转类型的板块距离。

rot\-min\-gauss0

\(0\.001\)要计算的力的高斯函数的最小值（截断值）（用于柔性轴势能）。

rot\-eps0

\(0\.0001\) \[nm^2 \]附加常数epsilon的值，用于rm2\*和flex2\*势能。

rot\-fit\-method0

\(rmsd\)确定旋转组的实际角度时所用的拟合方法（可用选项：rmsd，norm或potential）。

rot\-potfit\-nsteps0

\(21\)对于potential拟合类型，计算旋转势能所用的绕参考角的角度位置数。

rot\-potfit\-step0

\(0\.25\)对于potential拟合类型，两个角度位置之间的距离，以度为单位。

rot\-nstrout

\(100\)旋转组的角度，力矩以及旋转势能的输出频率（单位：步）。

rot\-nstsout

\(1000\)柔性轴势的每个板块数据，即角度，力矩和板块中心的输出频率。

### 5\.24 NMR 精修

disre

no

忽略拓扑文件中的距离限制信息

simple

简单（每个分子）的距离限制。

ensemble

一个模拟盒子中分子系综的距离限制。通常，可以使用mdrun \-multidir 对多个模拟进行系

综平均。环境变量GMX\_DISRE\_ENSEMBLE\_SIZE 设置每个系综中系统的数目（通常等于提供

给mdrun \-multidir的目录数）。

disre\-weighting

equal

将限制力平均分配到限制中的所有原子对上

conservative

力为限制势的导数，原子对的权重为正比于位移的负七次方。如果 disre\-tau ↪ 153 为零，力是

守恒的。

disre\-mixed

no

计算限制力时使用时间平均的偏离

yes

计算限制力时使用时间平均偏离和瞬时偏离乘积的平方根

disre\-fc

\(1000\) \[kJ mol\-1nm\-2\]距离限制的力常数，对每个限制可以乘上一个（可能）不同的因子，因子

在拓扑文件中相互作用的fac列中给出。

disre\-tau

\(0\) \[ps\]距离限制运行平均的时间常数。值为零时关闭时间平均。

nstdisreout

\(100\) \[步\]将限制所涉及的所有原子对之间的运行时间平均距离和瞬时距离，写入能量文件时的间

隔步数（可使能量文件变得非常大）

orire

no

忽略拓扑文件中的取向限制信息

yes

使用取向限制，可以使用mdrun \-multidir 进行系综平均

orire\-fc

\(0\) \[kJ mol\-1\]取向限制的力常数，每个限制可以乘上一个（可能）不同的权重因子。设置为零可

得到自由模拟时的取向

orire\-tau

\(0\) \[ps\]取向限制进行时间平均时间常数。值为零时关闭时间平均。

orire\-fitgrp

取向限制的叠合组。此原子组用于确定系统相对于参考取向的旋转矩阵 R 。参考取向为第一个子

系统的初始构象。对于蛋白质，骨架是一种合理的选择

nstorireout

\(100\) \[步\]将所有限制的运行时间平均取向和瞬时取向，以及分子序张量写入能量文件的间隔步数

（会使能量文件变得非常大）

### 5\.25 自由能计算

free\-energy

no

只使用拓扑A。

yes

在拓扑A\(lambda=0\)到拓扑B\(lambda=1\)之间插值，并将哈密顿量对lambda的导数

（由 dhdl\-derivatives ↪ 156 指定），或哈密顿量对其他lambda值的差值（由外部lambda指

定）输出到能量文件和/或dhdl\.xvg文件。这些文件可以用诸如 gmx bar ↪ 189 之类的程序进

行处理。如手册所述，对势能，键长和键角的插值是线性的。当 sc\-alpha ↪ 155 大于零时，会

对LJ和库仑相互作用使用软核势。

expanded

启用扩展系综模拟，其中转化状态变为动力学变量，允许在不同的哈密顿量之间跳跃。请参考扩展

系综的选项，它们控制了如何进行扩展系综模拟。扩展系综模拟中使用的不同哈密顿量由其他自

由能选项定义。

init\-lambda

\(\-1\) lambda的起始值（实数）。通常，此选项只能用于慢增长方法（即 delta\-lambda ↪ 154 非零的情

况）。在其他情况下，应该指定 init\-lambda\-state ↪ 154 。如果给定了lambda向量, init\-lambda

用于对向量进行内插而不是直接设定lambda\.必须大于或等于 0 。

delta\-lambda

\(0\) lambda每个时间步的增量

init\-lambda\-state

\(\-1\) lambda 状态的起始值（整数） 。指定应该使用 lambda 向量（ coul\-lambdas ↪ 154 ，

vdw\-lambdas ↪ 154 ， bonded\-lambdas ↪ 154 ， restraint\-lambdas ↪ 154 ， mass\-lambdas ↪ 154 ，

temperature\-lambdas ↪ 155 ， fep\-lambdas ↪ 154 ）的哪一列。这是一个从零开始的索引编号，

init\-lambda\-state=0表示使用第一列，依此类推。

fep\-lambdas

\[数组\]零个，一个或多个lambda值，会计算Delta H的值，并将其每 nstdhdl ↪ 156 步一次写入

dhdl\.xvg文件。值必须大于或等于 0 。允许使用大于 1 的值,但应该小心\.不同lambda值之间的

自由能差值可以使用 gmx bar ↪ 189 进行计算。 fep\-lambdas ↪ 154 与其他lambdas关键词不同，因为

未指定的lambda向量的所有分量都将使用 fep\-lambdas ↪ 154 （包括 restraint\-lambdas ↪ 154 ，因

此也包括牵引代码限制）。

coul\-lambdas

\[数组\]零个，一个或多个lambda值，会计算Delta H的值，并将其每 nstdhdl ↪ 156 步一次写入

dhdl\.xvg文件。值必须大于或等于 0 。允许使用大于 1 的值,但要小心\.如果使用软核势,值必

须介于 0 和 1 之间\. 只有静电相互作用由lambda向量的此分量控制（并且仅当lambda=0和

lambda=1的状态具有不同的静电相互作用时）。

vdw\-lambdas

\[数组\]零个，一个或多个lambda值，会计算Delta H的值，并将其每 nstdhdl ↪ 156 步一次写入

dhdl\.xvg文件。值必须大于或等于 0 。允许使用大于 1 的值,但要小心\.如果使用软核势,值必须

介于 0 和 1 之间。只有范德华相互作用由lambda向量的此分量控制。

bonded\-lambdas

\[数组\]零个，一个或多个lambda值，会计算Delta H的值，并将其每 nstdhdl ↪ 156 步一次写入

dhdl\.xvg文件。值必须大于或等于 0 。允许使用大于 1 的值,但要小心。只有成键相互作用由

lambda向量的此分量控制。

restraint\-lambdas

\[数组\]零个，一个或多个lambda值，会计算Delta H的值，并将其每 nstdhdl ↪ 156 步一次写入

dhdl\.xvg文件。值必须大于或等于 0 。允许使用大于 1 的值,但要小心。只有限制相互作用：二

面角限制，牵引代码限制由lambda向量的此分量控制。

mass\-lambdas

\[数组\]零个，一个或多个lambda值，会计算Delta H的值，并将其每 nstdhdl ↪ 156 步一次写入

dhdl\.xvg文件。值必须大于或等于 0 。允许使用大于 1 的值,但要小心。只有粒子质量由lambda

向量的此分量控制。

temperature\-lambdas

\[数组\]零个，一个或多个lambda值，会计算Delta H的值，并将其每 nstdhdl ↪ 156 步一次写入

dhdl\.xvg文件。值必须大于或等于 0 。允许使用大于 1 的值,但要小心。只有温度由lambda向

量的此分量控制。注意，这些lambda不能用于副本交换，只用于模拟回火。

calc\-lambda\-neighbors

\(1\)控制将计算和写出Delta H值的lambda值的数量，如果设置了 init\-lambda\-state ↪ 154 ，此

选项控制lambda值的数目，会计算相应的Delta H值并将其输出。选项为正值会将lambda点的

数目限制为只计算到 init\-lambda\-state ↪ 154 的第n个邻居。例如，如果 init\-lambda\-state ↪ 154

为 5 ，此参数值为 2 ，会计算lambda点3\-7并输出能量。此值为\-1表示输出所有lambda点。对

于普通的BAR，如 gmx bar ↪ 189 ，此值取 1 就足够了，而对于MBAR应该使用\-1。

sc\-function

\(beutler\)

beutler

Beutler等人的软核函数

gapsys

Gapsys等人的软核函数

sc\-alpha

\(0\)使用 sc\-function=beutler 时,软核势的alpha参数，值取 0 时对LJ和库仑相互作用进行线

性插值\.只能与 sc\-function=beutler 一起使用\.

sc\-r\-power

\(6\)软核势方程中径向项的次数。只能与 sc\-function=beutler 一起使用\.

2019:可能的值为 6 和 48 。 6 更标准，是默认值。使用 48 时，sc\-alpha通常应小得多（在0\.001

和0\.003之间）。

sc\-coul

\(no\)是否对分子的库仑相互作用使用软核自由能相互作用变换。默认值为no，因为在关闭范德华

相互作用之前线性地关闭库仑相互作用通常更有效。注意，只有在使用lambda状态时才考虑，而

不会用于 couple\-lambda0 ↪ 156 / couple\-lambda1 ↪ 156 ，你仍然可以通过将 sc\-alpha ↪ 155 设置为 0

来关闭软核相互作用。只能与 sc\-function=beutler 一起使用\.

sc\-power

\(1\)软核函数中lambda的次数，仅支持 1 和 2 \.只能与 sc\-function=beutler 一起使用\.

sc\-sigma

\(0\.3\) \[nm\]

对 sc\-function=beutler ,指定软核势的sigma值，用于那些C6或C12参数为零，或sigma小

于 sc\-sigma ↪ 155 的粒子\.只能与 sc\-function=beutler 一起使用\.

sc\-gapsys\-scale\-linpoint\-lj

\(0\.85\)对 sc\-function=gapsys ,此值为无量纲的alphaLJ参数\.它通过缩放vdw力的线性化点

来控制范德华相互作用的软硬程度。将其设置为 0 时，将产生标准的硬核范德华相互作用。只能

与 sc\-function=gapsys 一起使用\.

sc\-gapsys\-scale\-linpoint\-q

\(0\.3\) \[nm/e^2\]对于 sc\-function=gapsys ,此值对应alphaQ参数,单位为\[nm/e^2\],默认值为

0\.3\.它控制库仑相互作用的软硬程度\.将其设置为 0 时，将产生标准的硬核库仑相互作用。只能

与 sc\-function=gapsys 一起使用\.

sc\-gapsys\-sigma\-lj

\(0\.3\) \[nm\]对于 sc\-function=gapsys ,指定软核势的sigma值，用于那些C6或C12参数为零的

粒子\.只能与 sc\-function=gapsys 一起使用\.

couple\-moltype

这里可以设置计算溶剂化或耦合自由能的分子类型（拓扑中定义的）。特殊选项 system 用

于耦合系统中所有的分子类型。这对于平衡由（几乎）随机坐标开始的系统非常有用。必须

启用 free\-energy ↪ 153 选项。此分子类型中的范德华相互作用和/或电荷可以在lambda=0和

lambda=1之间打开或关闭，具体取决于 couple\-lambda0 ↪ 156 和 couple\-lambda1 ↪ 156 的设置。如

果要对多个分子副本中的一个去耦合，你需要复制并重命名拓扑中的分子定义。

couple\-lambda0

vdw\-q

在lambda=0时打开所有相互作用

vdw

在lambda=0时，电荷为零（无库仑相互作用）

q

在lambda=0时打开范德华相互作用；需要使用软核相互作用以避免奇点

none

在lambda=0时关闭范德华相互作用，并且电荷为零；需要使用软核相互作用以避免奇点。

couple\-lambda1

类似于 couple\-lambda0 ↪ 156 ，但用于lambda=1

couple\-intramol

no

分子类型 couple\-moltype ↪ 156 的所有分子内非键相互作用都被排除，或被以显式的配对相互

作用代替。以这种方式，分子的去耦合状态对应于无周期性效应的适当真空状态。

yes

也打开/关闭分子内的范德华和库仑相互作用。用于较大分子的分配自由能，这种情况下分子

内的非键相互作用可能导致分子被动力学地限制于真空构象。不会关闭1\-4配对相互作用。

nstdhdl

\(100\) dH/dlambda和可能的 Delta H写入 dhdl\.xvg 的频率， 0 表示不输出，此值应该

为 nstcalcenergy ↪ 128 的倍数。

dhdl\-derivatives

\(yes\)

如果为yes（默认值），每 nstdhdl ↪ 156 步输出一次哈密顿量对lambda的导数。使用 gmx bar ↪ 189

（尽管使用正确的外部lambda设置也可以做到，但可能不够灵活）或热力学积分对线性能量差值

进行内插时需要这些导数值。

dhdl\-print\-energy

\(no\)

在dhdl文件中包含总能量或势能。可用选项为no，potential或total。如果待研究的状态

处于不同的温度，后面进行自由能分析时需要该信息。如果所有状态都处于相同的温度，则不需要

此信息。如果使用mdrun \-rerun生成dhdl\.xvg文件，potential选项非常有用。当从现有的

轨迹重新运行时，动能往往是不正确的，因此必须单独使用势能来计算的残余的自由能，并解析地

计算动能分量。

separate\-dhdl\-file

yes

计算的自由能值（由外部lambda和 dhdl\-derivatives ↪ 156 指定）输出到一个单独的文件，

默认文件名称为dhdl\.xvg。 gmx bar ↪ 189 可以直接使用这个文件。

no

自由能的值输出到能量输出文件（ener\.edr，以累积块的形式，每 nstenergy ↪ 128 步一次），

可使用 gmx energy ↪ 237 或直接使用 gmx bar ↪ 189 来提取。

dh\-hist\-size

\(0\)如果为非零值，设定Delta H值（由外部lambda指定）和导数dH/dl值直方图的分格大小，

并写入ener\.edr。计算自由能差值时，这样做可以节省磁盘空间。对每个外部lambda输出一个

直方图，每个dH/dl输出两个直方图，每 nstenergy ↪ 128 步一次。注意，不正确的直方图设置（尺

寸太小或分格太宽）可能会导致错误。不要使用直方图，除非你确定自己需要它。

dh\-hist\-spacing

\(0\.1\)指定直方图的分格宽度，以能量为单位。与 dh\-hist\-size ↪ 157 一起使用。此大小限制了自由

能计算的精度。不要使用直方图，除非你确定自己需要它。

### 5\.26 扩展系综计算

nstexpanded

在扩展系综模拟中，两次尝试移动之间的积分步数，移动时会改变系统的哈密顿量。必须

为 nstcalcenergy ↪ 128 的倍数，但可以大于或小于 nstdhdl ↪ 156 。

lmc\-stats

no

不在状态空间中进行蒙特卡洛。

metropolis\-transition

使用Metropolis权重更新每个状态的扩展系综权重。Min\{1,exp\(\-\(beta\_new u\_new \- beta\_\-

old u\_old\)\}

barker\-transition

使用Barker转移判据更新每个状态i的扩展系综权重，定义为exp\(\-beta\_new u\_new\)/\(exp\(\-

beta\_new u\_new\)\+exp\(\-beta\_old u\_old\)\)。

wang\-landau

使用Wang\-Landau算法（在状态空间，而不是能量空间）来更新扩展系综的权重。

min\-variance

使用Escobedo等人的最小方差更新方法来更新扩展系综的权重。权重将不再是自由能，而是

更强调那些需要更多采样才能给出不确定度的状态。

lmc\-mc\-move

no

不在状态空间中进行蒙特卡洛。

metropolis\-transition

随机选择一个新的状态，向上或向下，然后使用Metropolis判据来决定接受还是拒绝：

Min\{1,exp\(\-\(beta\_new u\_new \- beta\_old u\_old\)\}

barker\-transition

随机选择一个新的状态，向上或向下，然后使用Barker转换判据来决定是接受还是拒绝：

exp\(\-beta\_new u\_new\)/\(exp\(\-beta\_new u\_new\)\+exp\(\-beta\_old u\_old\)\)

gibbs

使用给定坐标的状态的条件权重\(exp\(\-beta\_i u\_i\) / sum\_k exp\(beta\_i u\_i\)来决定移动到

哪个状态。

metropolized\-gibbs

使用给定坐标的状态的条件权重\(exp\(\-beta\_i u\_i\) / sum\_k exp\(beta\_i u\_i\)来决定移动到

哪个状态，排除当前状态，然后使用拒绝步来确保细致平衡。这种方法的效率总是比Gibbs

方法高，尽管在许多情况下只是略微高一些，例如当只有最近的邻区有相当大的相空间重叠

时。

lmc\-seed

\(\-1\)在状态空间进行蒙特卡洛移动时使用的随机种子。如果 lmc\-seed ↪ 158 设置为\-1，会使用伪随

机种子。

mc\-temperature

用于接受/拒绝蒙特卡洛移动的温度。如果未指定，会使用 ref\-t ↪ 137 的第一组中指定的模拟温度。

wl\-ratio

\(0\.8\) 要重置状态的占有率的直方图所用的截断值，自由能增量会从delta变为delta \*

wl\-scale ↪ 158 。如果我们定义Nratio = \(每个直方图的样本数\)/\(每个直方图的平均样本数\)。

wl\-ratio ↪ 158 为0\.8意味着，只有当所有Nratio> 0\.8并且同时所有1/Nratio > 0\.8时，才能认

为直方图是平坦的。

wl\-scale

\(0\.8\)每次当直方图被认为是平坦的时，自由能Wang\-Landau增量的当前值会乘以 wl\-scale ↪ 158 。

此值必须介于 0 和 1 之间。

init\-wl\-delta

\(1\.0\) Wang\-Landau增量的初始值，以kT为单位。接近1 kT的某些值通常最有效，尽管当自由

能差值很大时，有时取2\-3 kT的值会更好。

wl\-oneovert

\(no\)在大样本极限情况下，设置Wang\-Landau增量以1/\(模拟时间\)进行缩放。大量证据表明，

这里给出的状态空间中的标准Wang\-Landau算法会导致自由能“燃烧”到不正确的值，且取决于

初始状态。如果 wl\-oneovert ↪ 158 为yes，当增量小于1/N时，其中N为收集的样本数（因此正

比于数据收集时间，因而1/t），则将Wang\-Lambda增量设置为1/N，每步都减少。一旦发生这

种情况，会忽略 wl\-ratio ↪ 158 ，但当达到 lmc\-weights\-equil ↪ 159 设置的平衡判据后，权重仍将

停止更新。

lmc\-repeats

\(1\)控制每次迭代中执行每种蒙特卡洛交换类型的次数。在大量蒙特卡洛重复的极限情况下，所有

方法都收敛到吉布斯采样。此值通常不需要与 1 不同。

lmc\-gibbsdelta

\(\-1\)将吉布斯采样限制为选定的相邻状态数。对于吉布斯采样，对所有定义的状态进行采样有时效

率较低。 lmc\-gibbsdelta ↪ 159 取正值意味着在上下交换时只考虑加或减 lmc\-gibbsdelta ↪ 159 的

状态。值\-1意味着考虑所有的状态。如果状态数少于 100 ，包括所有的状态可能并没有那么耗时。

lmc\-forced\-nstart

\(0\)强制在初始状态空间进行采样以生成权重。为得到合理的初始权重，此设置允许模拟将系统从

初始lambda状态驱动到最终lambda状态，在每个状态进行 lmc\-forced\-nstart ↪ 159 步，然后移

动到下一个lambda状态。如果 lmc\-forced\-nstart ↪ 159 足够长（可能是数千步），权重就会接近

正确值。但是，在大多数情况下，简单地运行标准权重平衡算法可能更好。

nst\-transition\-matrix

\(\-1\)输出扩展系综转移矩阵的频率。负值表示在模拟结束时才会输出。

symmetrized\-transition\-matrix

\(no\)是否对称化经验转移矩阵。在无穷大的极限情况下，矩阵是对称的，但在短的时间尺度内会

因统计噪声而发散。通过使用矩阵T\_sym = 1/2 \(T \+ transpose\(T\)\)强制对称化，可以消除诸如

存在（小幅度的）负特征值之类的问题。

mininum\-var\-min

\(100\)最小方差策略（ lmc\-stats ↪ 157 选项）仅对大量样本有效，如果对每个状态使用的样本太少，

这个策略可能会失效。 mininum\-var\-min ↪ 159 设定每个状态在最小方差策略激活之前允许的最小

样本数。

init\-lambda\-weights

用于扩展系综态的初始权重（自由能）。默认值为零权重的向量。格式类似于 fep\-lambdas ↪ 154 中

的lambda向量设置，但权重可以是任何浮点数。单位为kT。其长度必须与lambdaxl长度匹配。

lmc\-weights\-equil

no

在整个模拟过程中不断更新扩展系综权重。

yes

输入的扩展系综权重被视为平衡值，在整个模拟过程中不更新。

wl\-delta

当Wang\-Landau增量低于此值时，停止更新扩展系综权重。

number\-all\-lambda

当所有lambda状态的样本数都大于此值时，停止更新扩展系综权重。

number\-steps

当步数大于此值指定的级别时，停止更新扩展系综权重。

number\-samples

当所有lambda状态的总采样数大于此值指定的级别时，停止更新扩展系综权重。

count\-ratio

当最小采样lambda状态和最大采样lambda状态的样本数之比大于该值时，停止更新扩展系

综权重。

simulated\-tempering

\(no\)启用或关闭模拟回火。模拟回火是通过扩展系综采样实现的，并使用不同的温度代替了不同

的哈密顿量。

sim\-temp\-low

\(300\) \[K\]模拟回火的低温值。

sim\-temp\-high

\(300\) \[K\]模拟回火的高温值。

simulated\-tempering\-scaling

控制从lambda向量的 temperature\-lambdas ↪ 155 部分计算中间lambda对应温度的方式。

linear

使用 temperature\-lambdas ↪ 155 的值对温度进行线性插值，即，如果 sim\-temp\-low ↪ 160 =300，

sim\-temp\-high ↪ 160 =400，则lambda=0\.5对应的温度为 350 。一组非线性的温度总可以使用

不均匀间距的lambda实现。

geometric

在 sim\-temp\-low ↪ 160 和 sim\-temp\-high ↪ 160 之间对温度进行几何插值。第i个状态的温度

为 sim\-temp\-low ↪ 160 \* \( sim\-temp\-high ↪ 160 / sim\-temp\-low ↪ 160 \)的\(i/\(ntemps\-1\)\)次方。对

恒定热容，这种方法应该给出大致相等的交换，尽管涉及蛋白质折叠的模拟具有非常高的热

容峰。

exponential

sim\-temp\-low ↪ 160 和 sim\-temp\-high ↪ 160 之 间 对 温 度 进 行 指 数 插

值。 第 i 个 状 态 的 温 度 为 sim\-temp\-low ↪ 160 \+ \( sim\-temp\-high ↪ 160 \-

sim\-temp\-low ↪ 160 \)\*\(\(exp\( temperature\-lambdas ↪ 155 \(i\)\)\-1\)/\(exp\(1\.0\)\-i\)\)。

### 5\.27 非平衡 MD

acc\-grps

具有恒定加速度的组，如Protein Sol，蛋白质和溶剂组中的所有原子都具有恒定的加速度，加

速度的值在 accelerate ↪ 160 中指定。注意，加速组质心的动能对体系的动能和温度都有贡献。如

果不希望这样，可将每个加速组都作为一个单独的温度耦合组。

accelerate

\(0\) \[nm ps\-2\] acc\-grps ↪ 160 组的加速度，对每个组需要指定x，y和z三个分量（如0\.1 0\.0 0\.0

\-0\.1 0\.0 0\.0表示第一组在X方向上具有0\.1 nm ps\-2的恒定加速度，第二组的加速度则相反）。

freezegrps

要冻结的组（即，它们的X，Y和/或Z位置不会更新；如Lipid SOL）。 freezedim ↪ 161 指定冻

结施加的维度。为避免完全冻结的原子之间过大的相互作用力对维里和压力的虚假贡献，你需要

使用能量组排除，这样做还能节省计算时间。注意，压力耦合算法不会缩放冻结原子的坐标。

freezedim

freezegrps ↪ 160 中的组应冻结的维度，为每个组的X，Y和Z方向指定Y或N（如Y Y N N N

N意味着第一组中的粒子只能沿Z方向移动。第二组中的粒子可以在任何方向移动）。

cos\-acceleration

\(0\) \[nm ps\-2\]计算粘度时加速度剖面的振幅。加速度沿X方向，大小为 cos\-acceleration ↪ 161 cos\(2

pi z/盒子长度\)。速度剖面的振幅以及粘度的倒数会输出到能量文件中。

deform

\(0 0 0 0 0 0\) \[nm ps\-1\]盒子元素的变形速率：a\(x\) b\(y\) c\(z\) b\(x\) c\(x\) c\(y\)。在模拟的每一步，

deform ↪ 161 非零的盒子元素的计算公式为box\(ts\)\+\(t\-ts\)\*deform，会根据周期性对非对角元素进

行校正。坐标也会相应地进行变换。冻结的自由度也会（有目的）变换。在第一步，以及将x和v

写入轨迹的那些步，时间ts会设置为t，这样可以确保精确地重启模拟。如果将适当的压缩系数

设置为零，变形可以与半各向同性或各向异性压力耦合一起使用。对角元素可用于固体应变。非对

角元素可用于固体或液体的剪切应变。

### 5\.28 电场

electric\-field\-x

electric\-field\-y

electric\-field\-z

在这里，你可以指定一个电场，并选择电场的交变性和脉冲。电场强度的一般表达式为高斯激光脉

冲形式：

𝐸\(𝑡\) = 𝐸 0 exp\[−\(𝑡 − 𝑡^0 \)

2

2𝜎^2 \]cos\[𝜔\(𝑡 − 𝑡^0 \)\]

例如，x 方向的四个参数在 electric\-field\-x ↪ 161 的字段中设置（electric\-field\-y 和

electric\-field\-z类似）

electric\-field\-x = E0 omega t0 sigma

单位分别为V nm\-1，ps\-1，ps，ps。

对于sigma = 0的特殊情况，会忽略指数项，只使用余弦项。在这种情况下,t0必须设为0\.如

果还设置了omega = 0，则会施加静电场。

。

### 5\.29 混合量子 / 经典分子动力学

QMMM\-grps

使用QM水平进行描述的组（也适用于MiMiC QM/MM）

QMMM

no

不使用QM/MM。

2023 版本不再通过以下\.mdp选项支持QM/MM\.对于MiMic,需要设置为no\.

yes

进行 QM/MM 模拟。可以在不同的 QM 水平上对几个组单独进行描述。这些组

在 QMMM\-grps ↪ 162 中指定，彼此间以空格隔开。各个组使用的从头算理论水平由 QMmethod ↪ 162

和 QMbasis ↪ 162 指定。只有使用由 QMMMscheme ↪ 162 指定的ONIOM QM/MM方案时，每个组

才能使用不同的理论水平。

QMMMscheme

normal

常规QM/MM。只能对一个 QMMM\-grps ↪ 162 组使用从头算理论进行描述，理论的水平

由 QMmethod ↪ 162 和 QMbasis ↪ 162 指定。系统的其余部分在MM水平进行描述。QM和MM

子系统的相互作用如下：MM部分的点电荷包含在QM部分的单电子哈密顿量中，所有

Lennard\-Jones相互作用都在MM水平进行描述。

ONIOM

使用Morokuma及其合作者发展的ONIOM方法描述子系统之间的相互作用。可以有不止

一个 QMMM\-grps ↪ 162 ，每个组可以使用不同水平的QM理论（ QMmethod ↪ 162 和 QMbasis ↪ 162 ）

进行描述。

QMmethod

\(RHF\)用于计算QM原子能量和梯度的方法。可用的方法包括AM1，PM3，RHF，UHF，

DFT，B3LYP，MP2，CASSCF和MMVB。对于CASSCF，活化空间中包含的电子数和轨

道数由 CASelectrons ↪ 162 和 CASorbitals ↪ 162 指定。

QMbasis

\(STO\-3G\)用于展开电子波函数的基组。目前只可以使用高斯基组，即STO\-3G，3\-21G，3\-21G\*，

3\-21\+G\*，6\-21G，6\-31G，6\-31G\*，6\-31\+G\*,和6\-311G。

QMcharge

\(0\) \[整数\] QMMM\-grps ↪ 162 的总电荷，单位 e 。如果有不止一个 QMMM\-grps ↪ 162 ，需要单独指定每个

ONIOM层的总电荷。

QMmult

\(1\) \[整数\] QMMM\-grps ↪ 162 的自旋多重度。如果有不止一个 QMMM\-grps ↪ 162 ，需要单独指定每个

ONIOM层的自旋多重度。

CASorbitals

\(0\) \[整数\]进行CASSCF计算时包含在活化空间中的轨道数。

CASelectrons

\(0\) \[整数\]进行CASSCF计算时包含在活化空间中的电子数。

SH

no

不使用势能面跳跃。系统始终处于电子基态。

yes

在激发态势能面上进行QM/MM MD模拟，在模拟过程中，如果系统遇到圆锥交叉点，强制

体系非绝热地跃到基态。此选项只能与CASSCF方法结合使用。

### 5\.30 计算电生理学

swapcoords

no

不启用离子/水位置交换。

X ; Y ; Z

沿所选方向进行离子/水位置交换。在膜平行于x\-y平面的典型设置中，需要在Z方向上交换

离子/水对，以维持腔室中所需的离子浓度。

swap\-frequency

\(1\)尝试交换的频率，即每隔多少个时间步，检查一次每个腔室的离子数目，并在必要时进行交换。

##### 5\.30\. 计算电生理学 163

##### 通常情况下，没有必要在每一个时间步都进行检查。对于典型的计算电生理学设置，大约 100 的

##### 值就足够了，并且对性能的影响可以忽略不计。

split\-group0

\#0通道的膜嵌入部分的索引组的名称。这些原子的质心限定了一个腔室的边界，应该选择质心靠

近膜中心的原子。

split\-group1

\#1通道定义了另一个腔室边界的位置。

massw\-split0

\(no\)是否使用质量权重来计算划分组的中心。

no

使用几何中心。

yes

使用质心。

massw\-split1

\(no\)如上所述，但用于\#1划分组。

solvent\-group

溶剂分子的索引组的名称。

coupl\-steps

\(10\)在指定数目的交换尝试步骤中，每个腔室的平均离子数。可用于防止腔室边界附近的离子（例

如沿通道扩散）导致不希望发生的来回交换。

iontypes

\(1\)要控制的不同离子的类型数。这些离子类型在模拟过程中会与溶剂分子进行交换，以达到所需

的参考数目。

iontype0\-name

第一种离子类型的名称。

iontype0\-in\-A

\(\-1\)腔室A中需要（参考）的 0 型离子的数目。默认值\-1表示：使用 0 时刻的离子数作为参考值。

iontype0\-in\-B

\(\-1\)腔室B中需要（参考）的 0 型离子的数目。

bulk\-offsetA

\(0\.0\)第一交换层相对于腔室A中分面的偏移量。默认情况下（即体相偏移= 0\.0），离子/水交换

发生在最大距离（体相浓度）层到划分组层之间。然而，可以指定偏移量b\(\-1\.0 < b < \+1\.0\)，将

体相层从中间0\.0处偏移到腔室分隔层之一（在\+/\-1\.0处）。

bulk\-offsetB

\(0\.0\)另一交换层相对于腔室B中分面的偏移量。

threshold

\(1\)只有达到指定的数目差异阈值时才交换离子。

cyl0\-r

\(2\.0\) \[nm\] \#0划分圆柱的半径。可以相对于划分组的中心定义两个可选的划分圆柱（以模拟通道

孔）。利用这些圆柱，可以统计哪些离子通过了哪个通道。划分圆柱的定义不会影响离子/水交换是

否完成。

cyl0\-up

\(1\.0\) \[nm\] \#0划分圆柱向上延伸的长度。

cyl0\-down

\(1\.0\) \[nm\] \#0划分圆柱向下延伸的长度。

cyl1\-r

\(2\.0\) \[nm\] \#1划分圆柱的半径。

cyl1\-up

\(1\.0\) \[nm\] \#1划分圆柱向上延伸的长度。

cyl1\-down

\(1\.0\) \[nm\] \#1划分圆柱向下延伸的长度。

### 5\.31 密度导向模拟

##### 这些选项启用并控制对额外力的计算和施加,这些力可由三维密度导出,如来自低温电子显微镜实验的密

##### 度。

density\-guided\-simulation\-active

\(no\)启用密度导向模拟\.

density\-guided\-simulation\-group

\(protein\)受密度导向模拟作用力影响,并对模拟密度有贡献的原子。

density\-guided\-simulation\-similarity\-measure

\(inner\-product\)根据原子位置计算出的密度与参考密度之间的相似度。

inner\-product

采用参考密度和模拟密度体素值的乘积之和。

relative\-entropy

使用参考密度和模拟密度之间的负相对熵（或Kullback\-Leibler散度）作为相似度。忽略负

密度值。

cross\-correlation

使用参考密度和模拟密度之间的Pearson相关系数作为相似度。

density\-guided\-simulation\-atom\-spreading\-weight

\(unity\)将原子分散到网格时,如何确定高斯核的乘子。

unity

密度拟合组中的每个原子都分配相同的单位因子。

mass

原子对模拟密度的贡献与其质量成正比。

charge

原子对模拟密度的贡献与其电荷成正比。

density\-guided\-simulation\-force\-constant

\(1e\+09\) \[kJ mol\-1\]密度导向模拟力的缩放因子\.也可以使用负值\.

density\-guided\-simulation\-gaussian\-transform\-spreading\-width

\(0\.2\) \[nm\]模拟密度扩散核的高斯RMS宽度。

density\-guided\-simulation\-gaussian\-transform\-spreading\-range\-in\-multiples\-of\-width

\(4\)高斯的截断范围,以上述高斯RMS宽度的倍数表示。

density\-guided\-simulation\-reference\-density\-filename

\(reference\.mrc\)参考密度文件的名称,使用绝对路径,或相对于调用gmx mdrun的文件夹的相对路

径。

density\-guided\-simulation\-nst

\(1\)计算和施加密度拟合力的间隔步数。施加时，拟合力会以此数值缩放（详情见参考手

册↪\.\./manual\-@GMX\_VERSION\_STRING@\.pdf）。

density\-guided\-simulation\-normalize\-densities

\(true\)将参考密度和模拟密度的密度体素值之和进行归一化。

density\-guided\-simulation\-adaptive\-force\-scaling

\(false\)调整力常数，确保模拟密度和参考密度之间的相似度稳步增加。

false

不使用自适应力缩放\.

true

使用自适应力缩放\.

density\-guided\-simulation\-adaptive\-force\-scaling\-time\-constant

\(4\) \[ps\]使用此时间常数耦合力常数,以增加与参考密度相似度。时间越大，耦合越松。

density\-guided\-simulation\-shift\-vector

\(0,0,0\) \[nm\]密度导向模拟中,在计算力和能量之前，将此向量添加到密度导向模拟组中的所有原

子上。仅影响密度导向模拟的力和能量。相当于将输入密度向相反方向偏移\(\-1\) \*密度导向模拟

偏移向量。

density\-guided\-simulation\-transformation\-matrix

\(1,0,0,0,1,0,0,0,1\)密度导向模拟中,在计算力和能量之前,将所有密度导向模拟组中的原子乘上此

矩阵\.只影响密度导向模拟的力和能量。相当于用该矩阵的逆矩阵对输入密度进行变换。矩阵以行

优先顺序给出。该选项用于实现某些操作,例如,以下输入可以将密度导向原子组绕z轴旋转𝜃度:

\(cos𝜃, −sin𝜃, 0,sin𝜃,cos𝜃, 0, 0, 0, 1\)\.

### 5\.32 使用 CP2K 接口的 QM/MM 模拟

##### 如果CP2K软件包链接到GROMACS，这些选项会启用并控制额外QM/MM力的计算和施加。有关

##### QM/MM接口实现的更多细节，请参阅使用 CP2K 进行混合量子经典模拟 \(QM/MM\)\.

qmmm\-cp2k\-active

\(false\)启用QM/MM模拟\.需要将CP2K链接到GROMACS\.

qmmm\-cp2k\-qmgroup

\(System\)索引组,其中的原子会使用QM进行处理\.

qmmm\-cp2k\-qmmethod

\(PBE\)描述体系QM部分所用的方法\.

PBE

DFT方法,使用PBE泛函和DZVP\-MOLOPT基组\.

BLYP

DFT方法,使用BLYP泛函和DZVP\-MOLOPT基组\.

INPUT

Provide an external input file for CP2K when running gmx grompp with the\-qmicommand\-

line option\. External input files are subject to the limitations that are described in Hybrid

Quantum\-Classical simulations \(QM/MM\) with CP2K interface\.

使用\-qmi命令行选项运行gmx grompp时,为CP2K提供外部输入文件。外部输入文件的

限制见使用 CP2K 进行混合量子经典模拟 \(QM/MM\) \.。

qmmm\-cp2k\-qmcharge

\(0\)\(0\) QM部分的总电荷\.

qmmm\-cp2k\-qmmultiplicity

\(1\)\(1\) QM部分的多重度或自旋态\.默认值 1 意味着单重态\.

qmmm\-cp2k\-qmfilenames

\(\)模拟过程中生成的CP2K文件的名称\.当使用默认的空值时，模拟输入文件的名称会带有额外

的\_cp2k后缀。

### 5\.33 用户自定义项

user1\-grps

user2\-grps

userint1 \(0\)

userint2 \(0\)

##### 5\.32\. 使用 CP2K 接口的 QM/MM 模拟 167

userint3 \(0\)

userint4 \(0\)

userreal1 \(0\)

userreal2 \(0\)

userreal3 \(0\)

userreal4 \(0\)

如果修改代码，可以使用这些选项。你可以传递整数，实数以及索引组到子程序。检查src/

gromacs/mdtypes/inputrec\.h中inputrec的定义

### 5\.34 移除的功能

这些功能已从GROMACS中移除，但为解析旧版本的 mdp ↪ 612 和 tpr ↪ 619 文件时不出现错误，GROMACS  
仍会解析这些选项。如果设置了这些选项， gmx grompp ↪ 252 和 gmx mdrun ↪ 276 会给出致命错误。

adress

\(no\)

implicit\-solvent

\(no\)

## 第 6 章命令行参考

GROMACS包括许多用于准备，运行和分析分子动力学模拟的工具。 ____gmx____ 对这些工具进行了封装，因  
此每个工具都是gmx的一部分，并通过类似 ____gmx grompp____ 或 ____gmx mdrun____ 这样的命令进行调用。2019:  
mdrun ↪ 276 是唯一一个可以单独构建↪ ____??____ 的二进制程序；在正常的构建中，它可以使用 ____gmx mdrun____ 运行。  
这些工具的文档可以在下面的相应章节以及手册页上找到（例如 gmx\-grompp\(1\) ），也可以使用 gmx  
help command 或gmx command \-h获取。

如果你安装了MPI版本的GROMACS，默认情况下 ____gmx____ 的名称为 ____gmx\_mpi____ ，所有工具都应该相应地  
进行调整。

### 6\.1 命令行界面和约定

##### 运行所有GROMACS命令时，在任何参数之前都需要指定一个选项（即，所有命令行参数的前面必须

##### 有一个以短划线开头的选项，不以短划线开头的值是前面选项的参数）。除布尔选项外，大多数选项都

##### 需要在其名称后面加上一个参数（或在某些情况下需要多个参数）。参数必须是一个单独的命令行参数，

即用空格隔开，如\-f traj\.xtc。如果需要为某一选项提供多个参数，应该将它们使用空格隔开。某些  
选项也有默认参数，即，指定不带任何参数的选项就会使用默认参数。如果根本没有指定某个选项，则  
会使用默认值；对于可选文件，默认情况可能是不使用该文件（参见下文）。

所有GROMACS命令选项都以单个短划线开头，无论它们是单字母选项还是多字母选项。但是，程序  
也可以识别双短划线（从5\.1版本开始）。

除了只用于特定命令的选项外，还有一些选项由 ____gmx____ 封装器处理，因此可用于任何命令。有关这类选项  
的列表，请参见命令行参考↪ 179 。这些选项无论放在命令名称之前（如 ____gmx \-quiet grompp____ ），还是放  
在命令名称之后（如 ____gmx grompp \-quiet____ ），都可以识别。还有一个 \-hidden选项可以与\-h 选项结  
合使用，用以显示针对高级/开发人员选项的帮助。

大多数分析命令可以处理原子数少于运行输入或结构文件的轨迹，但前提是轨迹由运行输入或结构文件  
的前 n 个原子组成。

#### 处理特定类型的命令行选项

布尔选项布尔选项的指定类似\-pbc，其否定形式的指定类似\-nopbc。也可以使用类似\-pbc no和  
\-pbc yes这样的显式指定。

文件名称选项接受文件名称的选项支持使用默认文件名称（将默认文件名称用于该选项）:

- 如果未设置所需选项，则使用默认值。
- 如果选项标记为可选，则除非设置了该选项（或其他条件使文件成为必需项），否则不会使用  
该文件。
- 如果设置了选项，但未提供文件名称，则使用默认值。  
所有这些选项都可以接受不带扩展名的文件名称。在这种情况下会自动追加扩展名。当接受多种  
输入格式时，例如通用结构格式，会在目录中查找具有提供名称或默认名称的每种类型的文件。如  
果找不到具有可识别扩展名的文件，就会报错。对于具有多种格式的输出文件，会使用默认文件类  
型。  
程序也可以从压缩（\.Z 或\.gz）文件中读取某些文件。

枚举选项枚举选项（enum）应使用选项指定列出的参数之一。参数可以缩写，程序会选择与列表中最  
短参数匹配的第一个参数。

向量选项某些选项接受向量值。可以提供 1 或 3 个参数；当只提供一个参数时，另外两个参数使用相  
同的值。

选区选项参见选区语法和用法↪ 371 。

### 6\.2 按名称排序的命令

gmx ↪ 179 ：分子动力学模拟程序

gmx anadock 2019 版工具↪ 179 ：根据Autodock的运行结果对结构进行聚类分析

gmx anaeig ↪ 180 ：分析特征向量/简正模式

gmx analyze ↪ 183 ：分析数据集

gmx angle ↪ 186 ：计算角度和二面角的分布以及相关

gmx awh ↪ 188 ：抽取加速权重直方图（AWH）运行的数据

gmx bar ↪ 189 ：使用Bennett接受率方法（BAR）计算自由能差的估计值

gmx bundle ↪ 191 ：分析轴束，例如螺旋

gmx check ↪ 192 ：检查并比较文件

gmx chi ↪ 194 ：计算chi和其他二面角的所有信息

gmx cluster ↪ 197 ：对结构进行聚类分析

gmx clustsize ↪ 200 ：计算原子团簇的尺寸分布

gmx confrms ↪ 202 ：叠合两个结构并计算RMSD

gmx convert\-tpr ↪ 203 ：生成修改后的运行输出文件

gmx convert\-trj ↪ 204 ：在不同轨迹类型之间进行转换

gmx covar ↪ 206 ：计算并对角化协方差矩阵

gmx current ↪ 207 ：计算介电常数和电流自相关函数

gmx density ↪ 209 ：计算体系的密度

gmx densmap ↪ 211 ：计算二维的平面或轴径向密度映射图

gmx densorder ↪ 213 ：计算表面涨落

gmx dielectric ↪ 214 ：计算频率相关的介电常数

gmx dipoles ↪ 216 ：计算总偶极及其涨落

gmx disre ↪ 218 ：分析距离限制

gmx distance ↪ 220 ：计算两个位置之间的距离

gmx do\_dssp 2019 工具↪ 225 ：指定二级结构并计算溶剂可及表面积

gmx dssp 2023 工具↪ 224 ：使用DSSP算法计算蛋白的二级结构

gmx dos ↪ 222 ：分析态密度及其相关性质

gmx dump ↪ 227 ：将二进制文件转换为人类可读的格式

gmx dyecoupl ↪ 229 ：从轨迹中抽取染料动力学

gmx dyndom 2019 工具↪ 230 ：结构旋转的内插和外推

gmx editconf ↪ 231 ：转换和操控结构文件

gmx eneconv ↪ 234 ：转换能量文件

gmx enemat ↪ 236 ：从能量文件中提取能量矩阵

gmx energy ↪ 237 ：将能量写入xvg文件并显示平均值

gmx extract\-cluster ↪ 241 ：从轨迹中抽取与团簇对应的帧

gmx filter ↪ 242 ：对轨迹进行频率滤波，用于制作平滑的动画

gmx freevolume ↪ 244 ：计算自由体积

gmx gangle ↪ 245 ：计算角度

gmx genconf ↪ 247 ：倍增随机取向的构象

gmx genion ↪ 249 ：在能量有利位置加入单原子离子

gmx genrestr ↪ 251 ：生成索引组的位置限制或距离限制

gmx grompp ↪ 252 ：生成运行输入文件

gmx gyrate ↪ 254 ：计算回旋半径

gmx h2order ↪ 256 ：计算水分子的取向

gmx hbond ↪ 257 ：计算分析氢键

gmx helix ↪ 260 ：计算𝛼螺旋结构的基本性质

gmx helixorient ↪ 261 ：计算螺旋内的局部螺距/弯曲/旋转/取向

gmx help ↪ 263 ：显示帮助信息

gmx hydorder ↪ 263 ：计算给定原子周围的四面体参数

gmx insert\-molecules ↪ 264 ：将分子插入已有空位

gmx lie ↪ 266 ：根据线性组合估计自由能

gmx make\_edi ↪ 267 ：生成本性动力学抽样的输入文件

gmx make\_ndx ↪ 270 ：制作索引文件

gmx mdmat ↪ 275 ：计算残基接触映射

gmx mdrun ↪ 276 ：执行模拟，简正分析或能量最小化

gmx mindist ↪ 280 ：计算两组间的最小距离

gmx mk\_angndx ↪ 282 ：生成用于gmx angle的索引文件

gmx morph 2019 工具↪ 283 ：构象间的线性内插

gmx msd ↪ 284 ：计算均方位移

gmx nmeig ↪ 286 ：对角化简正模式分析的Hessian矩阵

gmx nmens ↪ 288 ：根据简正模式生成结构系综

gmx nmr ↪ 289 ：根据能量文件分析核磁共振性质

gmx nmtraj ↪ 290 ：根据本征向量生成虚拟振荡轨迹

gmx nonbonded\-benchmark ↪ 291 ：非键成对内核的基准测试工具

gmx order ↪ 293 ：计算碳链尾部每个原子的序参量

gmx pairdist ↪ 295 ：计算位置索引组之间的成对距离

gmx pdb2gmx ↪ 297 ：将PDB坐标文件转换为拓扑文件以及与力场兼容的坐标文件

gmx pme\_error ↪ 300 ：根据给定的输入文件估计使用PME的误差

gmx polystat ↪ 301 ：计算聚合物的静态性质

gmx potential ↪ 302 ：计算沿盒子的静电势

gmx principal ↪ 304 ：计算一组原子的惯性主轴

gmx rama ↪ 305 ：计算Ramachandran图

gmx rdf ↪ 307 ：计算径向分布函数

gmx report\-methods ↪ 309 ：将模拟设置的简短摘要输出到文本文件和/或标准输出

gmx rms ↪ 309 ：计算与参考结构之间的RMSD及RMSD矩阵

gmx rmsdist ↪ 311 ：计算\-2，\-3或\-6次平均的原子对距离

gmx rmsf ↪ 313 ：计算原子涨落

gmx rotacf ↪ 314 ：计算分子的转动相关函数

gmx rotmat ↪ 316 ：计算叠合到参考结构的旋转矩阵

gmx saltbr ↪ 317 ：计算盐桥

gmx sans ↪ 318 ：计算小角中子散射谱

gmx sasa ↪ 320 ：计算溶剂可及表面积

gmx saxs ↪ 321 ：计算小角X射线散射谱

gmx select ↪ 322 ：输出选区的通用信息

gmx sham ↪ 325 ：根据直方图计算自由能或其他直方图

gmx sigeps ↪ 327 ：C6/12或C6/Cn组合与sigma/epsilon组合之间的相互转换

gmx solvate ↪ 328 ：体系溶剂化

gmx sorient ↪ 331 ：分析溶质周围的溶剂取向

gmx spatial ↪ 333 ：计算空间分布函数

gmx spol ↪ 335 ：分析溶质周围溶剂的偶极取向及极化

gmx tcaf ↪ 336 ：计算液体的粘度

gmx traj ↪ 337 ：输出轨迹文件中的坐标x，速度v，力f，盒子，温度和转动能

gmx trajectory ↪ 340 ：输出选区的坐标，速度和/或力

gmx trjcat ↪ 341 ：连接轨迹文件

gmx trjconv ↪ 343 ：转换和操控轨迹文件

gmx trjorder ↪ 347 ：根据到参考组的距离对分子排序

gmx tune\_pme ↪ 348 ：计算mdrun的运行时间与PME进程数的关系以优化设置

gmx vanhove ↪ 353 ：计算Van Hove位移及相关函数

gmx velacc ↪ 354 ：计算速度自相关函数

gmx view 2019 工具↪ 356 ：在X\-Windows终端显示轨迹

gmx wham ↪ 357 ：伞形抽样后进行加权直方分析

gmx wheel ↪ 361 ：绘制螺旋轮图

gmx x2top ↪ 361 ：根据坐标生成拓扑文件原型

gmx xpm2ps ↪ 363 ：将XPM（XPixelMap）矩阵转换为postscript或XPM

### 6\.3 按主题排序的命令

#### 6\.3\.1 分析轨迹

- gmx gangle ↪ 245 ：计算角度
- gmx convert\-trj ↪ 204 ：在不同轨迹类型之间进行转换
- gmx distance ↪ 220 ：计算两个位置之间的距离
- gmx dssp 2023 工具↪ 224 ：使用DSSP算法计算蛋白的二级结构
- gmx extract\-cluster ↪ 241 ：从轨迹中抽取与团簇对应的帧
- gmx freevolume ↪ 244 ：计算自由体积
- gmx msd ↪ 284 ：计算均方位移
- gmx pairdist ↪ 295 ：计算位置索引组之间的成对距离
- gmx rdf ↪ 307 ：计算径向分布函数
- gmx sasa ↪ 320 ：计算溶剂可及表面积
- gmx select ↪ 322 ：输出选区的通用信息
- gmx trajectory ↪ 340 ：输出选区的坐标，速度和/或力

#### 6\.3\.2 创建拓扑与坐标

- gmx editconf ↪ 231 ：编辑模拟盒子以及输出子组
- gmx x2top ↪ 361 ：根据坐标生成拓扑文件原型
- gmx solvate ↪ 328 ：体系溶剂化
- gmx insert\-molecules ↪ 264 ：将分子插入已有空位
- gmx genconf ↪ 247 ：倍增随机取向的构象
- gmx genion ↪ 249 ：在能量有利位置加入单原子离子
- gmx genrestr ↪ 251 ：生成索引组的位置限制或距离限制
- gmx pdb2gmx ↪ 297 ：将PDB坐标文件转换为拓扑文件以及与力场兼容的坐标文件

#### 6\.3\.3 运行模拟

- gmx grompp ↪ 252 ：生成运行输入文件
- gmx mdrun ↪ 276 ：执行模拟，简正分析或能量最小化
- gmx convert\-tpr ↪ 203 ：生成修改后的运行输出文件

#### 6\.3\.4 查看轨迹

- gmx nmtraj ↪ 290 ：根据本征向量生成虚拟振荡轨迹
- gmx view 2019 工具↪ 356 ：在X\-Windows终端显示轨迹

#### 6\.3\.5 处理能量

- gmx enemat ↪ 236 ：从能量文件中提取能量矩阵
- gmx energy ↪ 237 ：将能量写入xvg文件并显示平均值
- gmx mdrun ↪ 276 ：利用\-rerun选项（重新）计算轨迹中每帧的能量

##### 174 第 6 章 命令行参考

#### 6\.3\.6 转换文件

- gmx editconf ↪ 231 ：转换和操控结构文件
- gmx eneconv ↪ 234 ：转换能量文件
- gmx sigeps ↪ 327 ：C6/12或C6/Cn组合与sigma/epsilon组合之间的相互转换
- gmx trjcat ↪ 341 ：连接轨迹文件
- gmx trjconv ↪ 343 ：转换和操控轨迹文件
- gmx xpm2ps ↪ 363 ：将XPM（XPixelMap）矩阵转换为postscript或XPM

#### 6\.3\.7 工具

- gmx analyze ↪ 183 ：分析数据集
- gmx awh ↪ 188 ：抽取加速权重直方图（AWH）运行的数据
- gmx dyndom 2019 ↪ 230 ：结构旋转的内插和外推
- gmx filter ↪ 242 ：对轨迹进行频率滤波，用于制作平滑的动画
- gmx lie ↪ 266 ：根据线性组合估计自由能
- gmx morph 2019 ↪ 283 ：构象间的线性内插
- gmx pme\_error ↪ 300 ：根据给定的输入文件估计使用PME的误差
- gmx sham ↪ 325 ：根据直方图计算自由能或其他直方图
- gmx spatial ↪ 333 ：计算空间分布函数
- gmx traj ↪ 337 ：输出轨迹文件中的坐标x，速度v，力f，盒子，温度和转动能
- gmx tune\_pme ↪ 348 ：计算mdrun的运行时间与PME进程数的关系以优化设置
- gmx wham ↪ 357 ：伞形抽样后进行加权直方分析
- gmx check ↪ 192 ：检查并比较文件
- gmx dump ↪ 227 ：将二进制文件转换为人类可读的格式
- gmx make\_ndx ↪ 270 ：制作索引文件
- gmx mk\_angndx ↪ 282 ：生成用于gmx angle的索引文件
- gmx trjorder ↪ 347 ：根据到参考组的距离对分子排序
- gmx xpm2ps ↪ 363 ：将XPM（XPixelMap）矩阵转换为postscript或XPM
- gmx report\-methods ↪ 309 ：将模拟设置的简短摘要输出到文本文件和/或标准输出

#### 6\.3\.8 结构间的距离

- gmx cluster ↪ 197 ：对结构进行聚类分析
- gmx confrms ↪ 202 ：叠合两个结构并计算RMSD
- gmx rms ↪ 309 ：计算与参考结构之间的RMSD及RMSD矩阵
- gmx rmsf ↪ 313 ：计算原子涨落

#### 6\.3\.9 结构中的距离随时间的变化

- gmx mindist ↪ 280 ：计算两组间的最小距离
- gmx mdmat ↪ 275 ：计算残基接触映射
- gmx polystat ↪ 301 ：计算聚合物的静态性质
- gmx rmsdist ↪ 311 ：计算\-2，\-3或\-6次平均的原子对距离

#### 6\.3\.10 质量分布性质随时间的变化

- gmx gyrate ↪ 254 ：计算回旋半径
- gmx msd ↪ 284 ：计算均方位移
- gmx polystat ↪ 301 ：计算聚合物的静态性质
- gmx rdf ↪ 307 ：计算径向分布函数
- gmx rotacf ↪ 314 ：计算分子的转动相关函数
- gmx rotmat ↪ 316 ：计算叠合到参考结构的旋转矩阵
- gmx sans ↪ 318 ：计算小角中子散射谱
- gmx saxs ↪ 321 ：计算小角X射线散射谱
- gmx traj ↪ 337 ：输出轨迹文件中的坐标x，速度v，力f，盒子，温度和转动能
- gmx vanhove ↪ 353 ：计算Van Hove位移及相关函数

#### 6\.3\.11 分析成键相互作用

- gmx angle ↪ 186 ：计算角度和二面角的分布以及相关
- gmx mk\_angndx ↪ 282 ：生成用于gmx angle的索引文件

#### 6\.3\.12 结构性质

- gmx anadock 2019 工具↪ 179 ：根据Autodock的运行结果对结构进行聚类分析
- gmx bundle ↪ 191 ：分析轴束，例如螺旋
- gmx clustsize ↪ 200 ：计算原子团簇的尺寸分布
- gmx disre ↪ 218 ：分析距离限制
- gmx hbond ↪ 257 ：计算分析氢键
- gmx order ↪ 293 ：计算碳链尾部每个原子的序参量
- gmx principal ↪ 304 ：计算一组原子的惯性主轴
- gmx rdf ↪ 307 ：计算径向分布函数
- gmx saltbr ↪ 317 ：计算盐桥
- gmx sorient ↪ 331 ：分析溶质周围的溶剂取向
- gmx spol ↪ 335 ：分析溶质周围溶剂的偶极取向及极化

#### 6\.3\.13 动力学性质

- gmx bar ↪ 189 ：使用Bennett接受率方法（BAR）计算自由能差的估计值
- gmx current ↪ 207 ：计算介电常数和电流自相关函数
- gmx dos ↪ 222 ：分析态密度及其相关性质
- gmx dyecoupl ↪ 229 ：从轨迹中抽取染料动力学
- gmx principal ↪ 304 ：计算一组原子的惯性主轴
- gmx tcaf ↪ 336 ：计算液体的粘度
- gmx traj ↪ 337 ：输出轨迹文件中的坐标x，速度v，力f，盒子，温度和转动能
- gmx vanhove ↪ 353 ：计算Van Hove位移及相关函数
- gmx velacc ↪ 354 ：计算速度自相关函数

#### 6\.3\.14 静电性质

- gmx current ↪ 207 ：计算介电常数和电流自相关函数
- gmx dielectric ↪ 214 ：计算频率相关的介电常数
- gmx dipoles ↪ 216 ：计算总偶极及其涨落
- gmx potential ↪ 302 ：计算沿盒子的静电势
- gmx spol ↪ 335 ：分析溶质周围溶剂的偶极取向及极化
- gmx genion ↪ 249 ：在能量有利位置加入单原子离子

#### 6\.3\.15 蛋白质相关分析

- gmx do\_dssp 2019 工具↪ 225 ：指定二级结构并计算溶剂可及表面积
- gmx chi ↪ 194 ：计算chi和其他二面角的所有信息
- gmx helix ↪ 260 ：计算𝛼螺旋结构的基本性质
- gmx helixorient ↪ 261 ：计算螺旋内的局部螺距/弯曲/旋转/取向
- gmx rama ↪ 305 ：计算Ramachandran图
- gmx wheel ↪ 361 ：绘制螺旋轮图

#### 6\.3\.16 界面

- gmx bundle ↪ 191 ：分析轴束，例如螺旋
- gmx density ↪ 209 ：计算体系的密度
- gmx densmap ↪ 211 ：计算二维的平面或轴径向密度映射图
- gmx densorder ↪ 213 ：计算表面涨落
- gmx h2order ↪ 256 ：计算水分子的取向
- gmx hydorder ↪ 263 ：计算给定原子周围的四面体参数
- gmx order ↪ 293 ：计算碳链尾部每个原子的序参量
- gmx potential ↪ 302 ：计算沿盒子的静电势

#### 6\.3\.17 协方差分析

- gmx anaeig ↪ 180 ：分析特征向量
- gmx covar ↪ 206 ：计算并对角化协方差矩阵
- gmx make\_edi ↪ 267 ：生成本性动力学抽样的输入文件

#### 6\.3\.18 简正模式

- gmx anaeig ↪ 180 ：分析简正模式
- gmx nmeig ↪ 286 ：对角化简正模式分析的Hessian矩阵
- gmx nmtraj ↪ 290 ：根据本征向量生成虚拟振荡轨迹
- gmx nmens ↪ 288 ：根据简正模式生成结构系综
- gmx grompp ↪ 252 ：生成运行输入文件
- gmx mdrun ↪ 276 ：搜索势能极小点，计算Hessian矩阵

### 6\.4 命令说明

以下为各个命令的详细说明，也可参阅各个命令的手册页或使用gmx help 获知。

#### 6\.4\.1 gmx 分子动力学模拟程序

##### 概要

gmx \[ ____\-\[no\]h____ \] \[ ____\-\[no\]quiet____ \] \[ ____\-\[no\]version____ \] \[ ____\-\[no\]copyright____ \] \[ ____\-nice____ \]  
\[ ____\-\[no\]backup____ \]

##### 说明

##### GROMACS是一个功能齐全的程序，用于执行分子动力学模拟，即使用牛顿运动方程模拟具有数百到数

##### 百万粒子的系统的行为。它主要用于蛋白质，脂质和聚合物的研究，但也可用于研究广泛的化学和生物

##### 问题。

##### 选项

##### 控制选项

##### 选项 默认值 说明

\-\[no\]h no 输出帮助信息并退出

\-\[no\]quiet no 不输出常见的启动信息或引言

\-\[no\]version no 输出扩展版本信息并退出

\-\[no\]copyright no 启动时输出版权信息

\-nice <int> 19 指定运行级别（默认取决于命令）

\-\[no\]backup yes 如果存在输出文件则将其备份

#### gmx anadock\(2019\)

##### 概要

gmx anadock \[ ____\-f____ \[<\.pdb>\] \] \[ ____\-od____ \[<\.xvg>\] \] \[ ____\-of____ \[<\.xvg>\] \] \[ ____\-g____ \[<\.log>\] \]  
\[ ____\-xvg____ \] \[ ____\-\[no\]free____ \] \[ ____\-\[no\]rms____ \] \[ ____\-cutoff____ \]

##### 说明

gmx anadock用于分析Autodock程序的运行结果，并根据距离或RMSD对结构进行聚类分析。程序  
会分析对接能和自由能估计值，并打印每一聚类的能量统计数据。

也可以采用另一种方法，首先使用 gmx cluster ↪ 197 程序对结构进行聚类分析，然后按照最低能量或最低  
平均能量对聚类进行排序。

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

\-f

\[<\.pdb>\] eiwit\.pdb 蛋白质数据库文件

##### 输出文件选项

##### 选项 默认文件 类型 说明

\-od \[<\.xvg>\] edocked\.xvg xvgr/xmgr文件

\-of \[<\.xvg>\] efree\.xvg xvgr/xmgr文件

\-g \[<\.log>\] anadock\.log 日志文件

##### 控制选项

##### 选项 默认值 说明

\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none

\-\[no\]free no 使用Autodock的自由能估计值对聚类进行排序

\-\[no\]rms yes 根据RMS或距离进行聚类分析

\-cutoff <real> 0\.2 属于同一聚类的最大RMSD/距离

#### 6\.4\.2 gmx anaeig

##### 概要

gmx anaeig \[ ____\-v____ \[<\.trr/\.cpt/\.\.\.>\] \] \[ ____\-v2____ \[<\.trr/\.cpt/\.\.\.>\] \]  
\[ ____\-f____ \[<\.xtc/\.trr/\.\.\.>\] \] \[ ____\-s____ \[<\.tpr/\.gro/\.\.\.>\] \]  
\[ ____\-n____ \[<\.ndx>\] \] \[ ____\-eig____ \[<\.xvg>\] \] \[ ____\-eig2____ \[<\.xvg>\] \]  
\[ ____\-comp____ \[<\.xvg>\] \] \[ ____\-rmsf____ \[<\.xvg>\] \] \[ ____\-proj____ \[<\.xvg>\] \]  
\[ ____\-2d____ \[<\.xvg>\] \] \[ ____\-3d____ \[<\.gro/\.g96/\.\.\.>\] \]  
\[ ____\-filt____ \[<\.xtc/\.trr/\.\.\.>\] \] \[ ____\-extr____ \[<\.xtc/\.trr/\.\.\.>\] \]

____180____ 第 ____6____ 章 命令行参考

\[ \-over \[<\.xvg>\] \] \[ \-inpr \[<\.xpm>\] \] \[ \-b <time> \] \[ \-e <time> \]

\[ \-dt <time> \] \[ \-tu <enum> \] \[ \-\[no\]w \] \[ \-xvg <enum> \]

\[ \-first <int> \] \[ \-last <int> \] \[ \-skip <int> \] \[ \-max <real> \]

\[ \-nframes <int> \] \[ \-\[no\]split \] \[ \-\[no\]entropy \]

\[ \-temp <real> \] \[ \-nevskip <int> \]

##### 说明

gmx anaeig用于分析特征向量。特征向量可以来自协方差矩阵（ gmx covar ↪ 206 ）或简正模式分析（ gmx  
nmeig ↪ 286 ）。

当将轨迹投影到特征向量上时，如果存在，会将所有结构叠合到特征向量文件中的结构，否则会叠合到  
结构文件中的结构。如果没有提供运行输入文件，程序不会考虑周期性。大多数分析都是在从\-first  
到\-last的几个特征向量上进行的，但当\-first 设置为\-1时，程序会提示你选择要分析的特征向量。

\-comp:对从\-first到\-last的特征向量，给出其每个原子的向量分量。  
\-rmsf:对从\-first到\-last的特征向量，给出其每个原子的RMS波动（需要\-eig）。  
\-proj:计算轨迹在从\-first到\-last特征向量上的投影。轨迹在其协方差矩阵特征向量上的投影称  
为主成分（pc）。检查主成分的余弦含量通常很有用，因为随机扩散的主成分为余弦，其周期数等于主成  
分指数的一半。可以使用 gmx analyze ↪ 183 计算主成分的余弦含量。

\-2d:计算轨迹在\-first和\-last特征向量上的2d投影。  
\-3d:计算轨迹在前三个选定的特征向量上的3d投影。  
\-filt:对轨迹进行滤波，只显示其沿从\-first到\-last 特征向量的运动。  
\-extr:计算一条轨迹在平均结构上的两个极值投影，并在它们之间内插\-nframe帧，或使用 \-max设  
定需要的极值数目。会输出\-first特征向量，除非明确设置了\-first和\-last，在这种情况下，所  
有特征向量都会写入单独的文件。当输出 \.pdb ↪ 614 文件时，如果含有两个或三个结构，会添加链标识（你  
可以使用rasmol \-nmrpdb来查看这样的 \.pdb ↪ 614 文件）。

##### 协方差分析的重叠计算

##### 注意：分析时应使用相同的叠合结构

\-over:计算\-v2文件中的特征向量，与\-v文件中从\-first 到\-last的特征向量之间的子空间重  
叠。

\-inpr:计算\-v文件和\-v2文件中特征向量之间的内积矩阵。除非明确设置了\-first和\-last，否  
则会使用这两个文件中的所有特征向量。

如果指定了\-v和\-v2，会给出协方差矩阵之间重叠的单个数值。注意，默认情况下，会从特征向量输  
入文件中的时间戳字段读取特征值，但当指定\-eig或\-eig2 时，则会使用与其对应的特征值。计算  
公式为：

difference=sqrt\(tr\(\(sqrt\(M1\)\-sqrt\(M2\)\)^ 2 \)\)  
normalized overlap= 1 \- difference/sqrt\(tr\(M1\)\+tr\(M2\)\)  
shape overlap= 1 \- sqrt\(tr\(\(sqrt\(M1/tr\(M1\)\)\-sqrt\(M2/tr\(M2\)\)\)^ 2 \)\)

其中M1和M2为两个协方差矩阵，tr为矩阵的迹。给出的数值正比于波动平方根的重叠。归一化重叠

最有用，对全等矩阵，其值为 1 ，而当采样子空间正交时，其值为 0 。

当指定\-entropy选项时，会基于准简谐近似和Schlitter公式计算熵的估计值。

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

\-v \[<\.trr/\.cpt/\.\.\.>\] eigenvec\.trr 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，

tng ↪ 617

\-v2 \[<\.trr/\.cpt/\.\.\.>\] eigenvec2\.trr 可选 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，

tng ↪ 617

\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选

轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，

gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617

\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，

g96 ↪ 609 ， pdb ↪ 614 ，brk，ent

\-n \[<\.ndx>\] index\.ndx 可选 索引文件

\-eig \[<\.xvg>\] eigenval\.xvg 可选 xvgr/xmgr文件

\-eig2 \[<\.xvg>\] eigenval2\.xvg 可选 xvgr/xmgr文件

##### 输出文件选项

##### 选项 默认文件 类型 说明

\-comp \[<\.xvg>\] eigcomp\.xvg 可选 xvgr/xmgr文件

\-rmsf \[<\.xvg>\] eigrmsf\.xvg 可选 xvgr/xmgr文件

\-proj \[<\.xvg>\] proj\.xvg 可选 xvgr/xmgr文件

\-2d \[<\.xvg>\] 2dproj\.xvg 可选 xvgr/xmgr文件

\-3d \[<\.gro/\.g96/\.\.\.>\] 3dproj\.pdb 可选 结构文件： gro ↪^610 ， g96 ↪^609 ，

pdb ↪ 614 ，brk，ent，esp

\-filt \[<\.xtc/\.trr/\.\.\.>\] filtered\.xtc 可选

轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，

gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617

\-extr \[<\.xtc/\.trr/\.\.\.>\] extreme\.pdb 可选

轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，

gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617

\-over \[<\.xvg>\] overlap\.xvg 可选 xvgr/xmgr文件

\-inpr \[<\.xpm>\] inprod\.xpm 可选 X PixMap兼容的矩阵文件

##### 控制选项

##### 选项 默认值 说明

\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）

\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）

\-dt <time> 0

只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时

两帧之间的时间间隔（默认单位ps）

\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s

\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件

\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none

\-first <int> 1 要分析的第一个特征向量（\-1表示手动选择）

\-last <int> \-1 要分析的最后一个特征向量（\-1表示直到最后一个）

\-skip <int> 1 每隔指定数目的帧分析一次，即分析帧的间隔

\-max \(^0\) 特征向量在平均结构上的最大投影，指定 0 时给出极值  
\-nframes \(^2\) 输出极值的帧数  
\-\[no\]split no 时间为零时拆分特征向量投影  
\-\[no\]entropy no 根据准简谐公式或Schlitter方法计算熵。  
\-temp 298\.15 计算熵时的温度  
\-nevskip 6

##### 使用准简谐近似计算熵时要忽略的特征值的数目。在协方差分

##### 析之前进行转动和/或平动叠合时，会得到 3 或 6 个非常接近

##### 零的特征值，在计算熵时不应考虑这些特征值。

#### 6\.4\.3 gmx analyze

##### 概要

gmx analyze \[ \-f \[<\.xvg>\] \] \[ \-ac \[<\.xvg>\] \] \[ \-msd \[<\.xvg>\] \] \[ \-cc \[<\.xvg>\] \]

\[ \-dist \[<\.xvg>\] \] \[ \-av \[<\.xvg>\] \] \[ \-ee \[<\.xvg>\] \]

\[ \-fitted \[<\.xvg>\] \] \[ \-g \[<\.log>\] \] \[ \-\[no\]w \] \[ \-xvg <enum> \]

\[ \-\[no\]time \] \[ \-b <real> \] \[ \-e <real> \] \[ \-n <int> \] \[ \-\[no\]d \]

\[ \-bw <real> \] \[ \-errbar <enum> \] \[ \-\[no\]integrate \]

\[ \-aver\_start <real> \] \[ \-\[no\]xydy \] \[ \-\[no\]regression \]

\[ \-\[no\]luzar \] \[ \-temp <real> \] \[ \-fitstart <real> \]

\[ \-fitend <real> \] \[ \-filter <real> \] \[ \-\[no\]power \]

\[ \-\[no\]subav \] \[ \-\[no\]oneacf \] \[ \-acflen <int> \]

\[ \-\[no\]normalize \] \[ \-P <enum> \] \[ \-fitfn <enum> \]

\[ \-beginfit <real> \] \[ \-endfit <real> \]

##### 说明

gmx analyze可以读取一个ASCII文本文件并分析其中的数据集。输入文件中每行的第一个数据可以  
是时间（见\-time选项），后面跟着任意数目的 y 值。程序也可以读入多个数据集，它们之间以&符号  
（\-n选项）隔开；在这种情况下，对每一行，程序只会读入一个 y 值。程序会忽略所有以\#和@开头  
的行。所有的分析都可以用于数据集的导数（\-d选项）。  
除\-av和\-power外，所有选项都假定数据点之间的时间间隔是相等的。  
gmx analyze总会显示每一数据集的平均值和标准差，以及第三累积量和第四累积量的相对偏差，后二  
者都是相对于具有相同标准差的高斯分布计算的。  
选项\-ac计算自相关函数。请确保数据点之间的时间间隔远小于自相关的时间尺度  
选项\-cc给出数据集i与周期为i/2的余弦之间的相似性。计算公式为：

##### 6\.4\. 命令说明 183

2 \(integral ____from____ 0 to T of y\(t\) cos\(i pi t\) dt\)^ 2 /integral ____from____ 0 to T of y^ 2 \(t\) dt

这可用于由协方差分析得到的主成分，因为随机扩散的主要成分是单纯的余弦。

选项\-msd计算均方位移。

选项\-dist计算分布图。

选项\-av计算数据集的平均值。可以使用\-errbar选项得到平均值的误差限。误差限可以表示标准偏  
差，误差（假设各数据点是独立的），或是通过弃去顶部和底部5%的点而包含90%数据点的区间。

选项\-ee使用块平均估计误差。数据集被划分为多块，并计算每块的平均值。总平均值的误差根据m  
个块平均值B\_i之间的方差进行计算：error^2 = sum \(B\_i \- __\)^2 / \(m\*\(m\-1\)\)。程序会给出误差  
与块大小的函数关系。假定自相关是两个指数函数之和，程序还会给出解析的块平均值曲线。块平均值  
的解析曲线为：__

__f\(t\) = sigma \* sqrt\(2/T \( alpha \(tau\_1 \(\(exp\(\-t/tau\_1\) \- 1\) tau\_1/t \+ 1\)\) \+  
\(1\-alpha\) \(tau\_2 \(\(exp\(\-t/tau\_2\) \- 1\) tau\_2/t \+ 1\)\)\)\),__

__其中T为总时间。alpha，tau\_1和tau\_2通过将error^2拟合为f^2\(t\)得到。如果实际的块平均值非  
常接近解析曲线，误差为sigma\*sqrt\(2/T \(a tau\_1 \+ \(1\-a\) tau\_2\)\)。完整推导见B\. Hess, J\. Chem\.  
Phys\. 116:209\-217, 2002。__

__选项\-filter给出每个数据集和所有数据集相对于滤波平均值的RMS高频波动。滤波器正比于cos\(pi  
t/len\)，其中t从\-len/2到len/2。len由\-filter选项指定。此滤波器可以将周期为len/2和len的振  
荡分别降低为原来的79%和33%。__

__选项\-g使用\-fitfn 选项给出的函数对数据进行拟合。__

__选项\-power使用b t^a对数据进行拟合，这是通过在双对数标度下进行a t \+ b线性拟合实现的。拟  
合时，会忽略第一个零之后或负值之后的所有点。__

__选项 \-luzar 对 gmx hbond ↪ 257 的输出进行Luzar\-Chandler动力学分析。输入文件可以直接来自 gmx  
hbond \-ac，并应该得到与其相同的结果。__

__选项\-fitfn可用于拟合不同类型的曲线，这些曲线具有分子动力学背景，主要是指数曲线。更多信息  
见手册。为检查拟合过程的输出，可使用\-fitted选项将原始数据和拟合函数输出到新的数据文件中。  
拟合参数存放在输出文件的注释中。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f__

__\[<\.xvg>\] graph\.xvg xvgr/xmgr文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ac \[<\.xvg>\] autocorr\.xvg 可选 xvgr/xmgr文件__

__\-msd \[<\.xvg>\] msd\.xvg 可选 xvgr/xmgr文件__

__\-cc \[<\.xvg>\] coscont\.xvg 可选 xvgr/xmgr文件__

__\-dist \[<\.xvg>\] distr\.xvg 可选 xvgr/xmgr文件__

__\-av \[<\.xvg>\] average\.xvg 可选 xvgr/xmgr文件__

__\-ee \[<\.xvg>\] errest\.xvg 可选 xvgr/xmgr文件__

__\-fitted \[<\.xvg>\] fitted\.xvg 可选 xvgr/xmgr文件__

__\-g \[<\.log>\] fitlog\.log 可选 日志文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]time yes 输入数据的第一列为时间__

__\-b <real> \-1 读取数据集的起始时间__

__\-e <real> \-1 读取数据集的终止时间__

__\-n \(^1\) 读取指定数目的数据集，彼此间以&隔开  
\-\[no\]d no 使用导数  
\-bw 0\.1 分布的分格宽度  
\-errbar none \-av的误差限：none，stddev，error， 90  
\-\[no\]integrate no 使用梯形法对数据函数进行数值积分  
\-aver\_start \(^0\) 由此值开始对积分进行平均  
\-\[no\]xydy no 积分时将第二个数据集视为y值的误差  
\-\[no\]regression no  
对数据进行线性回归分析。如果设定了\-xydy选项，会  
将第二个数据集视为Y值的误差限。否则，如果存在多  
个数据集，则会进行多元线性回归，计算能使chi^2 = \(y__

- __A\_0 x\_0 \- A\_1 x\_1 \-\.\.\.\- A\_N x\_N\)^2取最小值的常  
数A，其中Y为输入文件中的第一个数据集，x\_i为其  
他数据集。请阅读\-time 选项的信息。__

__\-\[no\]luzar no__

__对由 gmx hbond ↪ 257 生成的相关函数及其数据进行__

__Luzar\-Chandler分析。如果指定了\-xydy选项，会将第__

__二列和第四列视为c\(t\)和n\(t\)的误差。__

__\-temp <real> 298\.15 进行Luzar氢键动力学分析时的温度（K）__

__\-fitstart <real> 1__

##### 为获得HB断裂和形成的前向和后向速率常数，拟合相关

__函数时的起始时间（ps）__

__\-fitend <real> 60__

##### 为获得HB断裂和形成的前向和后向速率常数，拟合相关

__函数时的终止时间（ps）。只能与\-gem选项一起使用__

__\-filter <real> 0 使用此长度的余弦滤波器进行滤波，然后输出高频波动__

__\-\[no\]power no 将数据拟合为b t^a__

__\-\[no\]subav yes 计算自相关前减去平均值__

__\-\[no\]oneacf no 对所有数据集计算一个ACF__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0 用于ACF的Legendre多项式的阶数（^0 表示不使用）:__

__0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit \(^0\) 对相关函数进行指数拟合的起始时间  
\-endfit \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

#### 6\.4\.4 gmx angle

##### 概要

__gmx angle \[ __\-f__ \[<\.xtc/\.trr/\.\.\.>\] \] \[ __\-n__ \[<\.ndx>\] \] \[ __\-od__ \[<\.xvg>\] \]  
\[ __\-ov__ \[<\.xvg>\] \] \[ __\-of__ \[<\.xvg>\] \] \[ __\-ot__ \[<\.xvg>\] \] \[ __\-oh__ \[<\.xvg>\] \]  
\[ __\-oc__ \[<\.xvg>\] \] \[ __\-or__ \[<\.trr>\] \] \[ __\-b__ \] \[ __\-e__ \]  
\[ __\-dt__ \] \[ __\-\[no\]w__ \] \[ __\-xvg__ \] \[ __\-type__ \]  
\[ __\-\[no\]all__ \] \[ __\-binwidth__ \] \[ __\-\[no\]periodic__ \]  
\[ __\-\[no\]chandler__ \] \[ __\-\[no\]avercorr__ \] \[ __\-acflen__ \]  
\[ __\-\[no\]normalize__ \] \[ __\-P__ \] \[ __\-fitfn__ \]  
\[ __\-beginfit__ \] \[ __\-endfit__ \]__

##### 说明

__gmx angle用于计算多个角或二面角的角度分布。__

__使用\-ov选项，可以得到一组角度的平均值与时间的函数关系。使用\-all选项时，输出文件的第一  
列为角度的平均值，其余为每个角度的值。__

__使用\-of选项，gmx angle会计算反式二面角的比例（仅适用于二面角）与时间的函数关系，但这可  
能只适用于少数选中的二面角。__

__使用\-oc选项，可以计算二面角的相关函数。__

__需要注意，对于角度，索引文件中必须包含原子三联对，对于二面角则必须包含原子四联对。否则，程  
序会崩溃。__

__使用\-or选项，可生成包含所选二面角的cos和sin函数值的轨迹文件，当使用 gmx covar ↪ 206 进行主  
成分分析时，此轨迹文件可以作为输入。__

__使用\-ot选项，可记录多重度为 3 的二面角旋转异构体之间的转变，假定输入轨迹各帧之间的时间间  
隔相等，可利用\-oh选项得到转变间隔时间的直方图。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] angle\.ndx 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-od \[<\.xvg>\] angdist\.xvg xvgr/xmgr文件__

__\-ov \[<\.xvg>\] angaver\.xvg 可选 xvgr/xmgr文件__

__\-of \[<\.xvg>\] dihfrac\.xvg 可选 xvgr/xmgr文件__

__\-ot \[<\.xvg>\] dihtrans\.xvg 可选 xvgr/xmgr文件__

__\-oh \[<\.xvg>\] trhisto\.xvg 可选 xvgr/xmgr文件__

__\-oc \[<\.xvg>\] dihcorr\.xvg 可选 xvgr/xmgr文件__

__\-or \[<\.trr>\] traj\.trr 可选 便携式xdr格式的轨迹__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

##### 读入轨迹最后一帧的时间，即分析的结束时间（默认单位

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-type <enum> angle 要分析的角度类型：angle，dihedral，improper，__

__ryckaert\-bellemans__

__\-\[no\]all no__

##### 按索引文件中的出现顺序，在平均值输出文件中单独列出每

##### 个角度的值

__\-binwidth \(^1\) 计算分布的分格宽度（单位度）  
\-\[no\]periodic yes 输出二面角除以 360 度的余数，即角度处于\[0, 360\)范围内  
\-\[no\]chandler no  
使用Chandler相关函数（N\[trans\] = 1，N\[gauche\] = 0）  
而不是余弦相关函数。转变定义为phi < \-60或phi > 60\.  
\-\[no\]avercorr no 对单个角度/二面角的相关函数进行平均  
\-acflen \-1 ACF的长度，默认为帧数的一半  
\-\[no\]normalize yes 归一化ACF  
\-P 0  
用于ACF的Legendre多项式的阶数（ 0 表示不使用）:  
0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit \(^0\) 对相关函数进行指数拟合的起始时间  
\-endfit \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

##### 已知问题

##### • 对转变进行计数仅适用于多重度为 3 的二面角

#### 6\.4\.5 gmx awh

##### 概要

__gmx awh \[ __\-f__ \[<\.edr>\] \] \[ __\-s__ \[<\.tpr>\] \] \[ __\-o__ \[<\.xvg>\] \] \[ __\-fric__ \[<\.xvg>\] \]  
\[ __\-b__ \] \[ __\-e__ \] \[ __\-\[no\]w__ \] \[ __\-xvg__ \] \[ __\-skip__ \]  
\[ __\-\[no\]more__ \] \[ __\-\[no\]kt__ \]__

##### 说明

__gmx awh用于从能量文件中提取AWH数据。每一时间帧每个AWH偏置会输出一个或两个文件。如果  
多于一个偏置索引，会将其追加到文件中，帧的时间也会追加。默认情况下，只输出PMF。如果指定了  
\-more选项，还会输出偏置，目标和坐标分布，以及使用sqrt\(det\(friction\_tensor\)\)归一化的度量，使  
得平均值为 1 。使用\-fric选项可以将摩擦张量的所有分量都输出到另一组文件中。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f__

__\[<\.edr>\] ener\.edr 能量文件__

__\-s__

__\[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] awh\.xvg xvgr/xmgr文件__

__\-fric \[<\.xvg>\] friction\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-skip__

__<int>^0 数据点之间跳过的帧数，即输出的帧间隔__

__\-\[no\]more no 输出更多信息__

__\-\[no\]kt no 以kT为单位输出自由能，而不是以kJ/mol为单位__

#### 6\.4\.6 gmx bar

##### 概要

__gmx bar \[ __\-f__ \[<\.xvg> \[\.\.\.\]\] \] \[ __\-g__ \[<\.edr> \[\.\.\.\]\] \] \[ __\-o__ \[<\.xvg>\] \]  
\[ __\-oi__ \[<\.xvg>\] \] \[ __\-oh__ \[<\.xvg>\] \] \[ __\-\[no\]w__ \] \[ __\-xvg__ \]  
\[ __\-b__ \] \[ __\-e__ \] \[ __\-temp__ \] \[ __\-prec__ \]  
\[ __\-nbmin__ \] \[ __\-nbmax__ \] \[ __\-nbin__ \] \[ __\-\[no\]extp__ \]__

##### 说明

__gmx bar通过Bennett接受率方法（BAR）计算自由能差的估计值。它也可以自动将由BAR得到的一  
系列单独的自由能进行加和，得到组合后的自由能估计值。__

__每个单独的BAR自由能差值依赖于两个不同状态下的模拟：且称为状态A和状态B，它们由参数  
lambda控制（参见 \.mdp ↪ 612 参数 init\_lambda）。BAR方法可以计算状态B与给定状态A的哈密顿  
量差值的加权平均的比率，反之亦然。在模拟过程中，必须明确地计算与其它状态的能量差。这可以通  
过 \.mdp ↪ 612 选项foreign\_lambda来实现。__

__输入选项\-f需要指定多个dhdl\.xvg文件。支持两种输入文件类型：__

- __包含多于一个 y 值的文件。这些文件中应包含dH/dlambda和Deltalambda的列。lambda的值  
根据图例推断：模拟使用的lambda根据dH/dlambda的图例推断，外部lambda的值根据Delta  
H的图例推断。__
- __只有一个 y 值的文件。对这些文件应该使用 \-extp选项，假定 y 值为dH/dlambda，并且哈密顿  
量与lambda成线性关系。模拟使用的lambda值根据副标题（如果存在）推断，否则会根据子目  
录下文件名中的数字推断。__

__模拟使用的lambda从dhdl\.xvg文件中包含字符串dH 的图例解析得到，外部lambda值则从包含大  
写字母D和H的图例解析得到。温度从包含T =的图例解析得到。__

__输入选项\-g 需要指定多个 \.edr ↪ 609 文件。它们可以包含能量差列表（参见 \.mdp ↪ 612 选项 separate\_\-  
dhdl\_file），或者一系列直方图（参见 \.mdp ↪ 612 选项 dh\_hist\_size和dh\_hist\_spacing）。程序会  
自动从ener\.edr文件中推断出温度和lambda值。__

__除了 \.mdp ↪ 612 的foreign\_lambda选项外，也可以从dH/dlambda值外推得到能量差。这可通过\-extp  
选项实现，它假定系统的哈密顿量与lambda呈线性关系，虽然通常并非如此。__

__自由能估计由使用二分法的BAR方法确定，输出精度由\-PREC设定。误差估计考虑了时间相关，这是  
通过将数据分块，并假定这些块相互独立，计算它们之间的自由能差来实现的。最终的误差估计由 5 个__

__块的平均方差确定。可以使用\-nbmin 和\-nbmax选项指定用于误差估计的分块编号的范围。__

__gmx bar会尝试合并具有相同自身和外部lambda值的样本，但始终假定样本相互独立。注意，当合并  
具有不同采样区间的能量差/导数时，这个假定几乎肯定不正确。后续的能量通常是相关的，不同的时间  
间隔意味着样本间的相关度不同。__

__结果分为两部分：后一部分包含了最终结果，单位为kJ/mol，以及每一部分和总体的误差估计。前一部  
分包含了详细的自由能差估计，以kT为单位的相空间重叠度（以及它们的误差估计）。输出值为：__

- __lam\_A: A点的lambda值。__
- __lam\_B: B点的lambda值。__
- __DG:自由能的估计值。__
- __s\_A: B在A中的相对熵估计值。__
- __s\_B: A在B中的相对熵估计值。__
- __stdev:每个样本标准偏差的估计值。__

__两个状态在彼此系综中的相对熵可以理解为相空间重叠的量度：lambda\_B的工作样本在lambda\_A系  
综中的相对熵s\_A（对s\_B反之亦然），是两个状态的Boltzmann分布之间’距离’的量度，当分布相  
同时，其值为零。更多信息见Wu & Kofke, J\. Chem\. Phys\. 123, 084109 \(2005\)。__

__每个样本标准偏差的估计，见Bennett BAR方法的原始论文Bennett, J\. Comp\. Phys\. 22, p 245 \(1976\)。  
其中的方程 10 给出了采样质量的估计（并非直接的实际统计误差，因为假定了样本相互独立）。__

__要得到相空间重叠的直观估计，可使用\-oh选项以及\-nbin选项输出一系列直方图。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xvg> \[\.\.\.\]\] dhdl\.xvg 可选 xvgr/xmgr文件__

__\-g \[<\.edr> \[\.\.\.\]\] ener\.edr 可选 能量文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] bar\.xvg 可选 xvgr/xmgr文件__

__\-oi \[<\.xvg>\] barint\.xvg 可选 xvgr/xmgr文件__

__\-oh \[<\.xvg>\] histogram\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-b <real> 0 BAR的起始时间__

__\-e <real> \-1 BAR的终止时间__

__\-temp <real> \-1 温度（K）__

__\-prec \(^2\) 小数点后的位数  
\-nbmin 5 用于误差估计的最小分块数  
\-nbmax 5 用于误差估计的最大分块数  
\-nbin 100 输出直方图的分格数  
\-\[no\]extp no 是否对dH/dl值进行线性外推以便用作能量__

#### 6\.4\.7 gmx bundle

##### 概要

__gmx bundle \[ __\-f__ \[<\.xtc/\.trr/\.\.\.>\] \] \[ __\-s__ \[<\.tpr/\.gro/\.\.\.>\] \] \[ __\-n__ \[<\.ndx>\] \]  
\[ __\-ol__ \[<\.xvg>\] \] \[ __\-od__ \[<\.xvg>\] \] \[ __\-oz__ \[<\.xvg>\] \]  
\[ __\-ot__ \[<\.xvg>\] \] \[ __\-otr__ \[<\.xvg>\] \] \[ __\-otl__ \[<\.xvg>\] \]  
\[ __\-ok__ \[<\.xvg>\] \] \[ __\-okr__ \[<\.xvg>\] \] \[ __\-okl__ \[<\.xvg>\] \]  
\[ __\-oa__ \[<\.pdb>\] \] \[ __\-b__ \] \[ __\-e__ \] \[ __\-dt__ \]  
\[ __\-tu__ \] \[ __\-xvg__ \] \[ __\-na__ \] \[ __\-\[no\]z__ \]__

##### 说明

__gmx bundle用于分析轴束。例如，可以分析螺旋轴组成的轴束。程序会读入两个索引组，并把它们分  
成\-na个部分。不同部分的质心定义了轴的顶部和底部。程序会计算以下几个量并将其输出到文件：轴  
的长度，轴中点相对于所有轴的平均中点的距离以及z方向的偏移量，轴相对于平均轴的总倾斜，径向  
倾斜以及侧向倾斜。__

__使用\-ok，\-okr和\-okl选项可输出轴的总扭折，径向扭折和侧向扭折。这种情况下还需要一个额外  
的索引组用以定义扭折原子，它也会被分成 \-na个部分。扭折角定义为扭折顶部和底部向量之间的夹  
角。__

__使用\-oa选项时，每帧中每个轴的顶点，中点（或扭折，若指定了\-ok）和底点会输出到一个 \.pdb ↪ 614  
文件。其中的残基编号对应于轴的编号。使用Rasmol查看这个文件时，可使用\-nmrpdb命令行选项，  
然后键入set axis true来显示参考轴。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ol \[<\.xvg>\] bun\_len\.xvg xvgr/xmgr文件__

__\-od \[<\.xvg>\] bun\_dist\.xvg xvgr/xmgr文件__

__\-oz \[<\.xvg>\] bun\_z\.xvg xvgr/xmgr文件__

__\-ot \[<\.xvg>\] bun\_tilt\.xvg xvgr/xmgr文件__

__\-otr__

__\[<\.xvg>\] bun\_tiltr\.xvg xvgr/xmgr文件__

__\-otl__

__\[<\.xvg>\] bun\_tiltl\.xvg xvgr/xmgr文件__

__\-ok \[<\.xvg>\] bun\_kink\.xvg 可选 xvgr/xmgr文件__

__\-okr__

__\[<\.xvg>\] bun\_kinkr\.xvg 可选 xvgr/xmgr文件__

__\-okl__

__\[<\.xvg>\] bun\_kinkl\.xvg 可选 xvgr/xmgr文件__

__\-oa \[<\.pdb>\] axes\.pdb 可选 蛋白质数据库文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧__

__之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-na <int> 0 轴的数目__

__\-\[no\]z no 使用 z 坐标轴作为参考轴，而不是使用平均轴__

#### 6\.4\.8 gmx check

##### 概要

__gmx check \[ __\-f__ \[<\.xtc/\.trr/\.\.\.>\] \] \[ __\-f2__ \[<\.xtc/\.trr/\.\.\.>\] \] \[ __\-s1__ \[<\.tpr>\] \]  
\[ __\-s2__ \[<\.tpr>\] \] \[ __\-c__ \[<\.tpr/\.gro/\.\.\.>\] \] \[ __\-e__ \[<\.edr>\] \]  
\[ __\-e2__ \[<\.edr>\] \] \[ __\-n__ \[<\.ndx>\] \] \[ __\-m__ \[<\.tex>\] \] \[ __\-vdwfac__ \]  
\[ __\-bonlo__ \] \[ __\-bonhi__ \] \[ __\-\[no\]rmsd__ \] \[ __\-tol__ \]  
\[ __\-abstol__ \] \[ __\-\[no\]ab__ \] \[ __\-lastener__ \]__

##### 192 第 6 章 命令行参考

##### 说明

__gmx check读入一个轨迹文件（ \.tng ↪ 617 ， \.trr ↪ 619 或 \.xtc ↪ 621 ），一个能量文件（ \.edr ↪ 609 ），或一个索引文  
件（ \.ndx ↪ 613 ）并输出与其相关的有用信息。__

__如果指定了\-c 选项，程序会检查文件中是否包含了坐标，速度和盒子信息，用于确定是否存在紧密接  
触（原子间距离小于\-vdwfac且没有键相连，即原子距离不介于\-bonlo和 \-bonhi之间。注意所有  
数值都是相对于两个原子范德华半径之和而言的），盒子外面是否存在原子（可能经常发生并不是什么  
问题）。如果文件中包含了速度，程序会根据速度计算温度的估计值。__

__如果指定了索引文件，程序会对其内容进行汇总。__

__如果同时指定了轨迹文件和 \.tpr ↪ 619 文件（使用\-s1选项），程序会检查tpr文件中定义的键长在轨迹  
中是否确实正确。如果不正确，这两个文件可能不匹配，原因可能出于去混洗或虚拟位点。通过这些选  
项，gmx check可以快速检查这些问题。__

__如果同时指定了\-s1和\-s2选项，程序还可以对比两个运行输入（ \.tpr ↪ 619 ）文件。当以这种方式比较  
运行输入文件时，会将默认的相对容差减小为0\.000001，绝对容差设置为零，以查找那些并非由于编译  
器优化的细微差别而导致的任何区别，当然你也可以通过选项设置任何其他容差。类似地，程序也可以  
对比两个轨迹文件（使用\-f2选项），或对比两个能量文件（使用 \-e2选项）。__

__对于自由能模拟，来自同一运行输入文件的A和B两种状态的拓扑可以通过\-s1和\-ab选项进行比  
较。指定了\-m选项，程序会输出一个LaTex文件，其内容可作为论文方法部分的粗略提纲。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-f2 \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s1 \[<\.tpr>\] top1\.tpr 可选 便携式xdr运行输入文件__

__\-s2 \[<\.tpr>\] top2\.tpr 可选 便携式xdr运行输入文件__

__\-c \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-e \[<\.edr>\] ener\.edr 可选 能量文件__

__\-e2 \[<\.edr>\] ener2\.edr 可选 能量文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-m__

__\[<\.tex>\] doc\.tex 可选 LaTeX文件__

__控制选项__

##### 选项 默认值 说明

__\-vdwfac <real> 0\.8 两原子VdW半径之和的比例，距离超过此值时会给出警告__

__\-bonlo <real> 0\.4 成键原子VdW半径之和的最小比例__

__\-bonhi <real> 0\.7 成键原子VdW半径之和的最大比例__

__\-\[no\]rmsd no 输出坐标，速度和力的RMSD__

__\-tol <real> 0\.001 相对容差2\*\(a\-b\)/\(|a|\+|b|\)，用于判断两个实数是否相等__

__\-abstol <real> 0\.001 绝对容差，用于两个数之和接近于零的情况__

__\-\[no\]ab no 比较同一文件中A和B状态的拓扑__

__\-lastener <string>__

##### 指定要对比的最后一个能量项（若未指定则测试所有项）。

__不检查此项之后的所有能量项。例如可以只对比Pressure__

__及其之前的能量项。__

#### 6\.4\.9 gmx chi

##### 概要

__gmx chi \[ \-s \[<\.gro/\.g96/\.\.\.>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-ss \[<\.dat>\] \]__

__\[ \-o \[<\.xvg>\] \] \[ \-p \[<\.pdb>\] \] \[ \-jc \[<\.xvg>\] \] \[ \-corr \[<\.xvg>\] \]__

__\[ \-g \[<\.log>\] \] \[ \-ot \[<\.xvg>\] \] \[ \-oh \[<\.xvg>\] \] \[ \-rt \[<\.xvg>\] \]__

__\[ \-cp \[<\.xvg>\] \] \[ \-b <time> \] \[ \-e <time> \] \[ \-dt <time> \] \[ \-\[no\]w \]__

__\[ \-xvg <enum> \] \[ \-r0 <int> \] \[ \-\[no\]phi \] \[ \-\[no\]psi \] \[ \-\[no\]omega \]__

__\[ \-\[no\]rama \] \[ \-\[no\]viol \] \[ \-\[no\]periodic \] \[ \-\[no\]all \] \[ \-\[no\]rad \]__

__\[ \-\[no\]shift \] \[ \-binwidth <int> \] \[ \-core\_rotamer <real> \]__

__\[ \-maxchi <enum> \] \[ \-\[no\]normhisto \] \[ \-\[no\]ramomega \]__

__\[ \-bfact <real> \] \[ \-\[no\]chi\_prod \] \[ \-\[no\]HChi \] \[ \-bmax <real> \]__

__\[ \-acflen <int> \] \[ \-\[no\]normalize \] \[ \-P <enum> \] \[ \-fitfn <enum> \]__

__\[ \-beginfit <real> \] \[ \-endfit <real> \]__

##### 说明

__gmx chi用于计算所有氨基酸主链和侧链的phi，psi，omega和chi二面角。它也可以计算二面角与时  
间的函数关系，以及二面角的直方图分布。分布（histo\-\(dihedral\)\(RESIDUE\)\.xvg）会对每一类型的  
所有残基进行累计。  
如果指定了 \-corr选项，程序会计算二面角的自相关函数C\(t\) = <cos\(chi\(tau\)\) cos\(chi\(tau\+t\)\)>。  
之所以使用余弦而不是角度自身，是为了解决周期性的问题（Van der Spoel & Berendsen  
\(1997\), Biophys\. J\. 72, 2032\-2041） 。程序会将每个残基的每个二面角输出到单独的文件  
（corr\(dihedral\)\(RESIDUE\)\(nresnr\)\.xvg）中，同时还会输出一个包含所有残基信息的文件（\-corr  
参数）。  
使 用 \-all 选 项， 程 序 会 将 每 个 残 基 的 角 度 与 时 间 的 函 数 关 系 输 出 到 单 独 的 文 件  
\(dihedral\)\(RESIDUE\)\(nresnr\)\.xvg。所用的单位可以是弧度或度。  
程序还会输出一个日志文件（\-g 选项）。其中包含__

- __每种类型的残基的数目信息。__
- __由Karplus方程得到的NMR ^3J耦合常数。__
- __一个表格，其中包含每个残基的旋转异构体每纳秒内的转变次数，以及每个二面角的序参数S^2。__
- __一个表格，其中包含每个残基的旋转异构体的占据率。__

__所有旋转异构体的多重度都视为 3 ，除了平面基团omega和chi二面角（即芳香族化合物，Asp和Asn  
的chi\_2; Glu和Gln的chi\_3;以及Arg的chi\_4），它们的多重度为 2 。rotamer 0表示二面角不处  
于每个旋转异构体的核心区域。核心区域的宽度可使用\-core\_rotamer指定。__

__S^2序参数也会输出到一个 \.xvg ↪ 623 文件（\-o 选项）中，作为可选，也可以将S^2的值作为B因子输  
出到一个 \.pdb ↪ 614 文件（\-p 选项）中。每个时间步旋转异构体的总转变次数（\-ot选项），每个旋转异  
构体的转变次数（\-rt选项）和^3J耦合（\-jc选项）也可以输出到 \.xvg ↪ 623 文件中。注意，在分析旋  
转异构体的转变时，假定所提供的轨迹帧之间的时间间隔是相同的。__

__如果指定了 \-chi\_prod 选项（并且 \-maxchi > 0），程序会累计旋转异构体，例如会计算  
1\+9\(chi\_1\-1\)\+3\(chi\_2\-1\)\+\(chi\_3\-1\)\(若残基有三个 3 重二面角并且 \-maxchi >= 3\)。如前所述，  
任何二面角如果不处于核心区域内，则其旋转异构体取为 0 。这些累计旋转异构体（从旋转异  
构体 0 开始）的占据率会输出到由 \-cp 选项指定的文件中，如果指定了 \-all 选项，旋转异  
构体与时间的函数关系会输出到 chiproduct\(RESIDUE\)\(nresnr\)\.xvg 文件，其占据率会输出到  
histo\-chiproduct\(RESIDUE\)\(nresnr\)\.xvg文件。__

__使用\-r选项可以生成平均omega角的等值线图，它是phi和psi角的函数，也就是说，在Ramachandran  
图中使用颜色编码绘制平均omega角。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.gro/\.g96/\.\.\.>\] conf\.gro 结构文件：brk，ent，esp gro ↪ tpr^610 ， g96 ↪^609 ， pdb ↪^614 ，__

__↪ 619__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-ss \[<\.dat>\] ssdump\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] order\.xvg xvgr/xmgr文件__

__\-p \[<\.pdb>\] order\.pdb 可选 蛋白质数据库文件__

__\-jc \[<\.xvg>\] Jcoupling\.xvg xvgr/xmgr文件__

__\-corr \[<\.xvg>\] dihcorr\.xvg 可选 xvgr/xmgr文件__

__\-g \[<\.log>\] chi\.log 日志文件__

__\-ot \[<\.xvg>\] dihtrans\.xvg 可选 xvgr/xmgr文件__

__\-oh \[<\.xvg>\] trhisto\.xvg 可选 xvgr/xmgr文件__

__\-rt \[<\.xvg>\] restrans\.xvg 可选 xvgr/xmgr文件__

__\-cp \[<\.xvg>\] chiprodhisto\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

读入轨迹第一帧的时间，即分析的起始时间（默认单位

__ps）__

__\-e <time> 0__

读入轨迹最后一帧的时间，即分析的结束时间（默认单

__位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即__

__分析时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-r0 <int> 1 起始残基编号__

__\-\[no\]phi no 输出phi二面角__

__\-\[no\]psi no 输出psi二面角__

__\-\[no\]omega no 输出omega二面角（肽键）__

__\-\[no\]rama no 生成phi/psi和chi\_1/chi\_2的Ramachandran图__

__\-\[no\]viol no 输出一个文件，根据是否违反Ramachandran规则对__

__角度指定 0 或 1__

__\-\[no\]periodic yes 输出二面角除以^360 度的余数，即角度处于\[0, 360\)范__

__围内__

__\-\[no\]all no 为每个二面角使用单独的输出文件__

__\-\[no\]rad no 在角度\-时间输出文件中，使用弧度而不是度作为单位__

__\-\[no\]shift no 根据phi/psi角度计算化学位移__

__\-binwidth <int> 1 直方图的分格宽度（单位：度）__

__\-core\_rotamer <real> 0\.5 只有中心的\-core\_rotamer\*\(360/multiplicity\)属于__

__每个旋转异构体（其余的分配给旋转异构体 0 ）__

__\-maxchi \(^0\) 计算前几个chi二面角： 0 ， 1 ， 2 ， 3 ， 4 ， 5 ， 6  
\-\[no\]normhisto yes 归一化直方图  
\-\[no\]ramomega no 计算omega的平均值与phi/psi的函数关系，并输出  
到 \.xpm ↪ 620 文件  
\-bfact \-1 \.pdb ↪^614 文件中的B因子值，用于那些没有计算二面角  
序参数的原子  
\-\[no\]chi\_prod no 对每个残基计算单个累计旋转异构体  
\-\[no\]HChi no 包括侧链氢原子的二面角  
\-bmax 0__

__构成二面角的任何原子的最大B因子，用于确定统计__

__中需要考虑的二面角。适用于分析多个X射线结构的__

__数据库工作。\-bmax<= 0意味着没有限制__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0 用于ACF的Legendre多项式的阶数（^0 表示不使用）__

__: 0 ， 1 ， 2 ， 3__

##### 196 第 6 章 命令行参考

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，__

__exp5，exp7，exp9__

__\-beginfit \(^0\) 对相关函数进行指数拟合的起始时间  
\-endfit \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结  
束__

##### 已知问题

##### • 会产生非常非常非常多的输出文件（最大数目约为蛋白质残基数的 4 倍，如果计算自相关函数则

##### 会变为 8 倍）。通常输出几百个文件。

- __使用非标准方式计算phi和psi二面角，使用H\-N\-CA\-C而不是C\(\-\)\-N\-CA\-C计算phi，使用  
N\-CA\-C\-O而不是N\-CA\-C\-N\(\+\)计算psi。这会导致计算结果与其他工具，如 gmx rama ↪ 305 的输  
出不一致（通常差异很小）。__
- __\-r0选项不能正常工作__
- __二重旋转异构体会输出到chi\.log，好像它们的多重度为 3 ，只不过第 3 个（g\(\+\)）的概率总是 0__

#### 6\.4\.10 gmx cluster

##### 概要

__gmx cluster \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-dm \[<\.xpm>\] \] \[ \-om \[<\.xpm>\] \] \[ \-o \[<\.xpm>\] \] \[ \-g \[<\.log>\] \]  
\[ \-dist \[<\.xvg>\] \] \[ \-ev \[<\.xvg>\] \] \[ \-conv \[<\.xvg>\] \]  
\[ \-sz \[<\.xvg>\] \] \[ \-tr \[<\.xpm>\] \] \[ \-ntr \[<\.xvg>\] \]  
\[ \-clid \[<\.xvg>\] \] \[ \-cl \[<\.xtc/\.trr/\.\.\.>\] \]  
\[ \-clndx \[<\.ndx>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-tu \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]dista \]  
\[ \-nlevels \] \[ \-cutoff \] \[ \-\[no\]fit \]  
\[ \-max \] \[ \-skip \] \[ \-\[no\]av \] \[ \-wcl \]  
\[ \-nst \] \[ \-rmsmin \] \[ \-method \]  
\[ \-minstruct \] \[ \-\[no\]binary \] \[ \-M \] \[ \-P \]  
\[ \-seed \] \[ \-niter \] \[ \-nrandom \]  
\[ \-kT \] \[ \-\[no\]pbc \]__

##### 说明

__gmx cluster可以使用几种不同的方法对结构进行聚类分析。结构之间的距离可以由轨迹确定，也可以  
从\-dm选项指定的 \.xpm ↪ 620 矩阵文件中读取。结构间的距离可以定义为叠合后的RMS偏差或原子对距  
离的RMS偏差。可用的聚类分析方法如下：__

__single linkage（单连接）:当一个结构到聚类中任何一个元素的距离小于 cutoff时，就将此结构加入  
聚类。__

__Jarvis Patrick:当一个结构和聚类中的某个结构互为相邻结构，并且它们至少具有P 个共同的相邻结构  
时，就将此结构加入聚类。一个结构的相邻结构是指距其最近的M个结构，或距其cutoff 之内的所  
有结构。__

__Monte Carlo（蒙特卡洛）:使用蒙特卡洛方法重新排序RMSD矩阵，使相邻帧之间的RMSD变化尽  
可能小。通过这种方式，可以使从一个结构到另一个结构的变化尽量平滑，并且彼此间具有最大可能的  
（例如）RMSD，但中间步骤的应尽可能小。这种方法可用于可视化模拟的平均力势系综或牵引模拟。显  
然，用户必须仔细地准备好轨迹（例如，不能存在叠加帧）。最终结果可以通过查看 \.xpm ↪ 620 矩阵文件进  
行直观地检查，此文件从下到上应该平滑地变化。  
diagonalization（对角化）:对角化RMSD矩阵。  
gromos: Daura等人介绍的算法（ Angew\. Chem\. Int\. Ed\. __1999__ , 38 , pp 236\-240）。使用截断来数算相  
邻结构的数目，将具有最多相邻结构的结构及其所有相邻结构作为一个聚类，并从聚类池中将这个聚类  
移除。然后对聚类池中剩余的结构重复以上操作。  
当聚类算法（single linkage, Jarvis Patrick和gromos）将每个结构都精确地分配到一个聚类，并且提供  
了轨迹文件时，程序会将每个聚类中，相对于其他结构，或平均结构，或所有结构具有最小平均距离的  
结构输出到轨迹文件。当输出所有结构时，会为每个聚类使用单独编号的文件。  
程序总会给出两个输出文件：__

- __\-o:输出一个矩阵，它的左上半部分为RMSD值，右下半部分为聚类的图形化描述。当\-minstruct  
= 1时，若两个结构属于同一聚类，相应的图像点为黑色。当\-minstruct> 1时，对每个聚类使  
用不同的颜色。__
- __\-g:输出所用选项的信息，以及所有聚类及其成员的详细列表。  
此外，程序也可以给出多个可选的输出文件：__
- __\-dist: RMSD的分布。__
- __\-ev: RMSD矩阵对角化的特征向量。__
- __\-sz:聚类的大小。__
- __\-tr:两个聚类之间转变次数的矩阵。__
- __\-ntr:从每个聚类或到每个聚类的总转变次数__
- __\-clid:聚类数目与时间的函数关系__
- __\-clndx:将聚类对应的帧编号输出到指定的索引文件，以便用于trjconv。__
- __\-cl:每个聚类的平均结构（\-av选项）或中心结构，或对所选的一组聚类，将其成员输出到带编  
号的文件（\-wcl选项，取决于\-nst和\-rmsmin选项）。聚类的中心是指其中与所有其他结构的  
平均RMSD最小的结构。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-dm \[<\.xpm>\] rmsd\.xpm 可选 X PixMap兼容的矩阵文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-om \[<\.xpm>\] rmsd\-raw\.xpm X PixMap兼容的矩阵文件__

__\-o \[<\.xpm>\] rmsd\-clust\.xpm X PixMap兼容的矩阵文件__

__\-g \[<\.log>\] cluster\.log 日志文件__

__\-dist \[<\.xvg>\] rmsd\-dist\.xvg 可选 xvgr/xmgr文件__

__\-ev \[<\.xvg>\] rmsd\-eig\.xvg 可选 xvgr/xmgr文件__

__\-conv \[<\.xvg>\] mc\-conv\.xvg 可选 xvgr/xmgr文件__

__\-sz \[<\.xvg>\] clust\-size\.xvg 可选 xvgr/xmgr文件__

__\-tr \[<\.xpm>\] clust\-trans\.xpm 可选 X PixMap兼容的矩阵文件__

__\-ntr \[<\.xvg>\] clust\-trans\.xvg 可选 xvgr/xmgr文件__

__\-clid \[<\.xvg>\] clust\-id\.xvg 可选 xvgr/xmgr文件__

__\-cl \[<\.xtc/\.trr/\.\.\.>\] clusters\.pdb 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-clndx \[<\.ndx>\] clusters\.ndx 可选 索引文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

读入轨迹最后一帧的时间，即分析的结束时间（默认单位

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]dista no 使用距离的RMSD而不是RMS偏差__

__\-nlevels <int> 40 离散化RMSD矩阵时所用的水平数__

__\-cutoff <real> 0\.1 定义两个相邻结构所用的RMSD截断值（nm）__

__\-\[no\]fit yes 计算RMSD前使用最小二乘叠合__

__\-max <real> \-1 RMSD矩阵的最大水平__

__skip \(^1\) 每隔指定数目的帧分析一次，即分析帧的间隔  
\-\[no\]av no 输出每一聚类的平均结构而不是中间结构  
\-wcl 0 将此数目的聚类包含的结构输出到编号文件中  
\-nst 1 一个聚类所含结构数目超过此数时，才会输出它的所有结构  
\-rmsmin \(^0\) 输出结构与其余聚类的最小rms差异__

__\-method <enum> linkage__

__聚类分析方法：linkage，jarvis\-patrick，__

__monte\-carlo，diagonalization，gromos__

__\-minstruct <int> 1 \.xpm ↪ 620 文件中着色聚类含有的最小结构数__

__\-\[no\]binary no 将RMSD矩阵转变为^0 和^1 矩阵，使用的截断值由__

__\-cutoff指定__

__\-M <int> 10 Jarvis\-Patrick算法使用的最近相邻结构数，取^0 时使用截__

__断值__

__\-P <int> 3 形成聚类所需的相同最近结构数__

__\-seed \(^0\) 蒙特卡洛聚类算法的随机数种子（ 0 表示自动生成）  
\-niter \(^10000\) 蒙特卡洛的迭代次数  
\-nrandom 0 蒙特卡洛的第一次迭代可以完全随机地进行，以对帧进行混  
洗  
\-kT 0\.001 蒙特卡洛优化使用的Boltzmann权重因子（取^0 会禁用爬  
升步骤）  
\-\[no\]pbc yes PBC检查__

#### 6\.4\.11 gmx clustsize

##### 概要

__gmx clustsize \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xpm>\] \] \[ \-ow \[<\.xpm>\] \] \[ \-nc \[<\.xvg>\] \]  
\[ \-mc \[<\.xvg>\] \] \[ \-ac \[<\.xvg>\] \] \[ \-hc \[<\.xvg>\] \]  
\[ \-temp \[<\.xvg>\] \] \[ \-mcn \[<\.ndx>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-\[no\]w \] \[ \-xvg \]  
\[ \-cut \] \[ \-\[no\]mol \] \[ \-\[no\]pbc \] \[ \-nskip \]  
\[ \-nlevels \] \[ \-ndf \] \[ \-rgblo \]  
\[ \-rgbhi \]__

##### 说明

__gmx clustsize用以计算气相中分子/原子团簇的尺寸分布。计算结果以 \.xpm ↪ 620 文件的形式给出。团  
簇的总数会输出到一个 \.xvg ↪ 623 文件。__

__如果指定\-mol选项，计算团簇时会以分子而不是原子为基本单元，这样可以对大分子进行团簇化。在  
这种情况下，索引文件中仍然应当包含原子编号，否则计算会以SEGV终止。__

__当轨迹包含速度时，程序假定所有粒子都可以自由移动，并将最大团簇的温度输出到一个单独的 \.xvg ↪ 623  
文件中。如果使用了约束，则需要校正温度。例如，使用SHAKE或SETTLE算法模拟水时，得到的  
温度是正常温度的1/1\.5。你可以使用\-ndf选项来补偿这一点。请记住，计算时要移除质心的运动。__

__使用\-mcn选项会输出一个索引文件，其中包含最大团簇的原子编号。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 可选 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xpm>\] csize\.xpm X PixMap兼容的矩阵文件__

__\-ow \[<\.xpm>\] csizew\.xpm X PixMap兼容的矩阵文件__

__\-nc \[<\.xvg>\] nclust\.xvg xvgr/xmgr文件__

__\-mc \[<\.xvg>\] maxclust\.xvg xvgr/xmgr文件__

__\-ac \[<\.xvg>\] avclust\.xvg xvgr/xmgr文件__

__\-hc \[<\.xvg>\] histo\-clust\.xvg xvgr/xmgr文件__

__\-temp \[<\.xvg>\] temp\.xvg 可选 xvgr/xmgr文件__

__\-mcn \[<\.ndx>\] maxclust\.ndx 可选 索引文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-cut <real> 0\.35 一个团簇中的最大距离（nm）__

__\-\[no\]mol no 对分子而不是原子进行团簇分析（需要 \.tpr ↪ 619 文件）__

__\-\[no\]pbc yes 使用周期性边界条件__

__\-nskip \(^0\) 两次输出之间跳过的帧数，即输出的帧间隔  
\-nlevels 20 \.xpm ↪ 620 输出文件中的灰度等级数  
\-ndf \-1 计算温度时整个系统的自由度数。如果未设置，使用的值为原  
子数的 3 倍  
\-rgblo  
1 1 0 团簇大小最低值的RGB颜色值__

__\-rgbhi__

__<vector> 0 0 1 团簇大小最高值的RGB颜色值__

#### 6\.4\.12 gmx confrms

##### 概要

__gmx confrms \[ \-f1 \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-f2 \[<\.gro/\.g96/\.\.\.>\] \]__

__\[ \-n1 \[<\.ndx>\] \] \[ \-n2 \[<\.ndx>\] \] \[ \-o \[<\.gro/\.g96/\.\.\.>\] \]__

__\[ \-no \[<\.ndx>\] \] \[ \-\[no\]w \] \[ \-\[no\]one \] \[ \-\[no\]mw \] \[ \-\[no\]pbc \]__

__\[ \-\[no\]fit \] \[ \-\[no\]name \] \[ \-\[no\]label \] \[ \-\[no\]bfac \]__

##### 说明

__gmx confrms 首先将第二个结构最小二乘叠合到第一个结构，然后计算两个结构的均方根偏差  
（RMSD）。两个结构的原子数不必相同，只要用于叠合的两个索引组具有相同的原子数即可。使用  
\-name选项时，只使用所选组中名称匹配的原子进行叠合和RMSD计算。当比较蛋白质的突变体时，这  
个功能可能用得上。  
叠合的结构会输出到一个 \.pdb ↪ 614 文件中。在这个文件中，两个结构会作为单独的模型（可使用rasmol  
\-nmrpdb查看）。使用\-bfac选项时，根据原子的RMSD值计算的B因子也会输出到这个 \.pdb ↪ 614 中。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f1 \[<\.tpr/\.gro/\.\.\.>\] conf1\.gro 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-f2 \[<\.gro/\.g96/\.\.\.>\] conf2\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp tpr ↪ 619__

__\-n1 \[<\.ndx>\] fit1\.ndx 可选 索引文件__

__\-n2 \[<\.ndx>\] fit2\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.gro/\.g96/\.\.\.>\] fit\.pdb 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp__

__\-no \[<\.ndx>\] match\.ndx 可选 索引文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-\[no\]one no 只将叠合后的结构输出到文件__

__\-\[no\]mw yes 叠合和RMSD计算时使用质量加权__

__\-\[no\]pbc no 尽量将分子恢复完整__

__\-\[no\]fit yes 将目标结构与参考结构进行最小二乘叠合__

__\-\[no\]name no 叠合和RMSD计算时只考虑名称匹配的原子__

__\-\[no\]label no 添加链标识，第一个结构为A，第二个结构为B__

__\-\[no\]bfac no 根据原子的MSD值输出B因子__

#### 6\.4\.13 gmx convert\-tpr

##### 概要

__2019: gmx convert\-tpr \[ __\-s__ \[<\.tpr>\] \] \[ __\-n__ \[<\.ndx>\] \] \[ __\-o__ \[<\.tpr>\] \]  
\[ __\-extend__ \] \[ __\-until__ \] \[ __\-nsteps__ \]  
\[ __\-\[no\]zeroq__ \]__

__2023: gmx convert\-tpr \[ __\-s__ \[<\.tpr/\.gro/\.\.\.>\] \] \[ __\-n__ \[<\.ndx>\] \]  
\[ __\-o__ \[<\.tpr/\.gro/\.\.\.>\] \] \[ __\-extend__ \] \[ __\-until__ \]  
\[ __\-nsteps__ \] \[ __\-\[no\]generate\_velocities__ \]  
\[ __\-velocity\_temp__ \] \[ __\-velocity\_seed__ \]__

##### 说明

__gmx convert\-tpr能以三种方式编辑修改运行输入文件：__

____1\.__ 修改运行输入文件中的模拟步数，可使用选项\-extend，\-tiltil或\-nsteps（nsteps=\-1表示不  
限制步数）  
__2\.__ 为原始tpx文件的一部分创建\.tpx文件，当想要删除\.tpx文件中的溶剂，或者创建一个例如只包含  
Calpha的\.tpx文件时，可使用这个功能。注意，你可能需要使用 \-nsteps \-1（或类似的选项）才能  
达到目的。警告：此 __\.tpx__ 文件功能不全。  
__3\.__ 将指定组的电荷设置为零。当使用LIE（线性相互作用能）方法估计自由能时，此功能很有用。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 要修改的运行输入文件: tprgrog96pdb brk__

__ent__

__\-n \[<\.ndx>\] index\.ndx 可选 包含额外索引组的文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.tpr/\.gro/\.\.\.__

__>\]__

__tprout\.tpr 可选 生成的运行输入文件: tprgrog96pdb brk ent__

##### 控制选项

##### 选项 默认值 说明

__\-extend <time> 0 将模拟运行时间延长指定值（ps）__

__\-until \(^0\) 将模拟运行时间延长至指定值（ps）  
\-nsteps 0 更改剩余的模拟步数  
\-\[no\]generate\_velocities no 重新指定速度，使用生成的种子，除非明确设  
置了种子  
\-velocity\_temp \(^300\) 生成速度时所用的温度  
\-velocity\_seed \-1 生成速度的随机种子\.若设为\-1,则生成一个  
新的种子\.__

#### 6\.4\.14 gmx convert\-trj\(2023\)

##### 概要

__gmx convert\-trj \[ __\-f__ \[<\.xtc/\.trr/\.\.\.>\] \] \[ __\-s__ \[<\.tpr/\.gro/\.\.\.>\] \]  
\[ __\-n__ \[<\.ndx>\] \] \[ __\-o__ \[<\.xtc/\.trr/\.\.\.>\] \] \[ __\-b__ \]  
\[ __\-e__ \] \[ __\-dt__ \] \[ __\-tu__ \]  
\[ __\-fgroup__ \] \[ __\-xvg__ \] \[ __\-\[no\]rmpbc__ \]  
\[ __\-\[no\]pbc__ \] \[ __\-sf__ \] \[ __\-selrpos__ \]  
\[ __\-select__ \] \[ __\-vel__ \] \[ __\-force__ \]  
\[ __\-atoms__ \] \[ __\-precision__ \] \[ __\-starttime__ \]  
\[ __\-timestep__ \] \[ __\-box__ \]__

##### 说明

__gmx convert\-trj 可以对不同格式的轨迹文件进行转换。该模块可以根据支持的输入格式输出所有  
GROMACS支持的文件格式。__

__该模块还提供了一系列可能修改单个轨迹帧的选项，包括生成更小输出文件的选项。它还可以用结构文  
件中的粒子信息替换输入轨迹中存储的粒子信息。__

__该模块还可以根据用户提供的选区生成轨迹的子集。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型: xtctrrcptgrog96__

__pdbtng__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构: tprgrog96pdb brk ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xtc/\.trr/\.\.\.>\] trajout\.xtc 输出轨迹: xtctrrcptgrog96pdbtng__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时__

__间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束__

__时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧__

__时间的帧，即分析时两帧之间的时间间隔__

__（默认单位ps）__

__\-tu <enum> ps 时间值的单位: fs, ps, ns, us, ms, s__

__\-fgroup__

__<selection>__

##### 轨迹文件中存储的原子\(若未设定,则假

##### 定为前N个原子\)

__\-xvg <enum> xmgrace 绘图格式: xmgrace, xmgr, none__

__\-\[no\]rmpbc yes 保证每一帧的分子都完整__

__\-\[no\]pbc yes 计算距离时应用周期性边界条件__

__\-sf <file> 使用文件提供选区__

__\-selrpos <enum> atom__

__选区参考位置: atom, res\_com, res\_cog,__

__mol\_com, mol\_cog, whole\_res\_com,__

__whole\_res\_cog, whole\_mol\_com,__

__whole\_mol\_cog, part\_res\_com,__

__part\_res\_cog, part\_mol\_com,__

__part\_mol\_cog, dyn\_res\_com,__

__dyn\_res\_cog, dyn\_mol\_com,__

__dyn\_mol\_cog__

__\-select__

__<selection> 将指定选区的粒子写入文件__

__\-vel <enum> preserved\-if\-present__

##### 如果可能,保存帧中粒子的速度:

__preserved\-if\-present, always, never__

__\-force <enum> preserved\-if\-present__

##### 如果可能,保存帧中粒子的力:

__preserved\-if\-present, always, never__

__\-atoms <enum> preserved\-if\-present__

##### 新的原子信息来自拓扑还是当前帧：

__preserved\-if\-present,__

__always\-from\-structure, never, always__

__\-precision \(^3\) 输出值的精度  
\-starttime \(^0\) 修改第一帧的起始时间  
\-timestep 0 修改不同帧之间的间隔时间  
\-box 输出帧所用的新的对角盒向量__

#### 6\.4\.15 gmx covar

__概要__

__gmx covar \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-v \[<\.trr/\.cpt/\.\.\.>\] \]  
\[ \-av \[<\.gro/\.g96/\.\.\.>\] \] \[ \-l \[<\.log>\] \] \[ \-ascii \[<\.dat>\] \]  
\[ \-xpm \[<\.xpm>\] \] \[ \-xpma \[<\.xpm>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-xvg \] \[ \-\[no\]fit \]  
\[ \-\[no\]ref \] \[ \-\[no\]mwa \] \[ \-last \] \[ \-\[no\]pbc \]__

##### 说明

__gmx covar用于计算并对角化（质量加权的）协方差矩阵。所有结构都叠合到结构文件中的结构。如果  
结构文件不是运行输入文件，程序不会考虑周期性。如果叠合组与分析组相同，而且分析组未使用质量  
加权，则叠合时也不使用质量加权。__

__特征向量会输出到一个轨迹文件（\-v 选项指定）。如果叠合与协方差分析所用的原子相同，会首先输出  
用于叠合的参考结构，其对应的时刻t=\-1。输出的平均（或参考，若指定了 \-ref选项）结构对应的  
t=0，特征向量会写入不同的帧，以特征向量编号作为步数，特征值作为时间戳。__

__特征向量可使用 gmx anaeig ↪ 180 进行分析。__

__使用\-ascii选项可以将整个协方差矩阵输出到一个ASCII文件。矩阵元素的输出顺序为：x1x1，x1y1，  
x1z1，x1x2，\.\.\.__

__使用\-xpm选项可以将整个协方差矩阵输出到一个 \.xpm ↪ 620 文件。__

__使用\-xpma选项可以将原子的协方差矩阵输出到一个 \.xpm ↪ 620 文件，即输出每对原子xx，yy和zz协  
方差的总和。__

__注意，矩阵的对角化所需内存和时间至少正比于所涉及原子数的平方。因此很容易耗尽内存，在这种情  
况下，程序很可能会出现段错误并退出。你应该仔细考虑能否减少要分析的原子数目，这样可以降低计  
算成本。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr__

__结构\+质量（db）: tpr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] eigenval\.xvg xvgr/xmgr文件__

__\-v \[<\.trr/\.cpt/\.\.\.>\] eigenvec\.trr 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，__

__tng ↪ 617__

__\-av \[<\.gro/\.g96/\.\.\.>\] average\.pdb 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，__

__brk，ent，esp__

__\-l \[<\.log>\] covar\.log 日志文件__

__\-ascii \[<\.dat>\] covar\.dat 可选 通用数据文件__

__\-xpm \[<\.xpm>\] covar\.xpm 可选 X PixMap兼容的矩阵文件__

__\-xpma \[<\.xpm>\] covara\.xpm 可选 X PixMap兼容的矩阵文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧__

__之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]fit yes 叠合到参考结构__

__\-\[no\]ref no 使用结构文件中的构象而不是平均构象来计算偏差__

__\-\[no\]mwa no 质量加权的协方差分析__

__\-last__

__<int> \-1 输出的最后一个特征向量的编号（\-1会输出所有特征向量）__

__\-\[no\]pbc yes 对周期性边界条件进行修正__

#### 6\.4\.16 gmx current

##### 概要

__gmx current \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \]__

__\[ \-o \[<\.xvg>\] \] \[ \-caf \[<\.xvg>\] \] \[ \-dsp \[<\.xvg>\] \]__

__\[ \-md \[<\.xvg>\] \] \[ \-mj \[<\.xvg>\] \] \[ \-mc \[<\.xvg>\] \] \[ \-b <time> \]__

__\[ \-e <time> \] \[ \-dt <time> \] \[ \-\[no\]w \] \[ \-xvg <enum> \]__

__\[ \-sh <int> \] \[ \-\[no\]nojump \] \[ \-eps <real> \] \[ \-bfit <real> \]__

__\[ \-efit <real> \] \[ \-bvit <real> \] \[ \-evit <real> \]__

__\[ \-temp <real> \]__

##### 说明

__gmx current用于计算电流自相关函数，系统转动偶极矩和平动偶极矩的相关，以及由此得到的静态介  
电常数。为得到合理的结果，索引组必须是电中性的，总电荷为零。进一步，如果给出了速度，程序也  
可以根据电流自相关函数计算静态电导率。此外，可以使用Einstein\-Helfand拟合得到静态电导率。__

__\-caf选项用于指定电流自相关函数的输出文件，\-mc选项用于指定偶极矩转动和平动相关的输出文件。  
但这一选项只适用于含有速度的轨迹。指定\-sh和\-tr选项可以对自相关函数进行平均和积分。由于  
平均是通过偏移轨迹的起始点进行的，因此可以使用\-sh选项来修改偏移，以便能够选择不相关的起  
始点。当接近终点时，统计的精度会降低，因此对相关函数的积分只进行到某个点，这样才能得到可靠  
的值，具体的点数取决于帧的数目。计算静态介电常数时，可以使用\-tr选项控制要考虑的积分区域。__

__选项\-temp指定计算静态介电常数所需的温度。__

__如果模拟中使用了反应场或偶极修正Ewald求和（\-eps=0对应于圆罐边界条件），可以使用\-eps选  
项指定周围介质的介电常数。__

__使用\-\[no\]nojump选项可以取消坐标折叠，允许离子自由扩散。这样才能得到连续的动偶极矩以便进  
行Einstein\-Helfand拟合。拟合结果可用于确定带电分子系统的介电常数。然而，也可以根据折叠坐标  
对应的总偶极矩波动计算介电常数。但使用此选项时必须小心，因为只有在非常短的时间跨度内才能满  
足分子密度近似恒定且平均值收敛的近似条件。为保险起见，计算介电常数时，应使用Einstein\-Helfand  
方法计算其平动部分。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] current\.xvg xvgr/xmgr文件__

__\-caf__

__\[<\.xvg>\] caf\.xvg 可选 xvgr/xmgr文件__

__\-dsp__

__\[<\.xvg>\] dsp\.xvg xvgr/xmgr文件__

__\-md \[<\.xvg>\] md\.xvg xvgr/xmgr文件__

__\-mj \[<\.xvg>\] mj\.xvg xvgr/xmgr文件__

__\-mc \[<\.xvg>\] mc\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两__

__帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-sh \(^1000\) 对相关函数和均方位移进行平均时偏移的帧数。  
\-\[no\]nojump yes 移除跨过盒子的原子跳跃。  
\-eps 0 周围介质的介电常数。值为 0 时相当于无穷大（圆罐边界条件）。  
\-bfit 100 平动偶极矩MSD拟合为直线时的起始值。  
\-efit 400 平动偶极矩MSD拟合为直线时的终止值。  
\-bvit 0\.5 电流自相关函数拟合为at^b时的起始值。  
\-evit \(^5\) 电流自相关函数拟合为at^b时的终止值。  
\-temp 300 计算介电常数epsilon时所用的温度。__

#### 6\.4\.17 gmx density

##### 概要

__gmx density \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-s \[<\.tpr>\] \]  
\[ \-ei \[<\.dat>\] \] \[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-d \]  
\[ \-sl \] \[ \-dens \] \[ \-ng \] \[ \-\[no\]center \]  
\[ \-\[no\]symm \]__

##### 说明

__gmx density用于计算整个盒子的局部密度，需要使用索引文件。__

__对于NPT模拟的总密度，可以直接使用 gmx energy ↪ 237 得到。__

__使用\-center选项可以基于绝对的盒子坐标，相对于任意组的中心进行直方图分格。如果要计算沿Z  
轴方向的密度剖面，设盒子Z方向的长度为bZ，当基于整个系统进行居中时，那么输出的坐标范围  
为\-bZ/2到bZ/2。注意，这种作法是从GROMACS 5\.0开始的；早期版本只是在\(0, bZ\)范围内进行简  
单的静态分格，并将输出进行偏移。而现在程序会计算每一帧的中心，并在\(\-bZ/2, bZ/2\)范围内进行  
分格。__

__指定\-symm选项可以使输出结果关于中心对称。这会自动启用\-center选项。__

__总是以相对盒子坐标进行分格，以考虑到盒子尺寸会随压力耦合而变化，输出时会按输出轴方向的平均  
盒子长度进行缩放\.__

__密度的单位为kg/m^3，也可以计算数密度或电子密度。计算电子密度时，需要使用\-ei选项提供一个  
文件，其中包含了每种类型原子的电子数。文件的内容类似下面：__

__2  
atomname=nrelectrons  
atomname=nrelectrons__

__第一行指明了该文件需要读取的行数。系统中每个唯一的原子名称都对应一行。每个原子的电子数会根  
据其原子的部分电荷进行修改。__

__双层系统的重要注意事项__

__最常见的使用场景之一是计算跨脂质双层的各种原子组的密度，通常以z轴作为法线方向。对于短时间  
的模拟，小的系统，固定的盒子尺寸，上面的作法很适用，但对于更一般的情况，脂质双层可能比较复  
杂。第一个问题是，尽管蛋白质和脂质的体积压缩率都比较低，但脂质的面积压缩率相当高。这意味着  
即便是完全弛豫好的系统，在模拟过程中盒子形状（厚度和每个脂质分子占据的面积）也会发生很大的  
波动。由于GROMACS将盒子置于原点和正坐标值之间，这反过来意味着由于这些波动，位于盒子中  
心的双层会向上/向下移动一点，并进而模糊密度剖面。解决这个问题的最简单方法（如果你需要使用  
压力耦合）是使用\-center选项来计算相对于盒子中心的密度剖面。注意，即使你有一个复杂的非对  
称系统，带有双层以及比如说膜蛋白，你仍然可以将双层部分作为中心，这样得到的输出只是在（中心）  
原点参考的某一侧具有更多的值。__

__最后，对不受表面张力影响的大的双层系统，在系统中形成“波浪”的地方会表现出起伏波动。这是生  
物系统的基本性质，如果要与实验结果进行比较，你可能希望考虑这种起伏模糊效应。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-ei \[<\.dat>\] electrons\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] density\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两__

__帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-d <string> Z 指定膜的法线方向，X，Y或Z__

__\-sl \(^50\) 将盒子划分为指定数目的切片  
\-dens mass 密度类型：mass，number，charge，electron  
\-ng 1 要计算密度的组的数目  
\-\[no\]center no 相对于（变化的）盒子中心进行分格。适用于双层  
\-\[no\]symm no 使密度相对于中心沿轴方向对称。适用于双层__

##### 已知问题

##### • 计算电子密度时，使用了原子名称而不是原子类型。这种作法不好。

##### 补充说明

__gmx density是获取体系或各个组分在盒子内分布密度的一个程序。一般来说可使用类似下面的命令：__

__gmx density \-f File\.trr \-n File\.ndx \-s File\.tpr \-d z \-o density\.xvg__

__其中\-f指定要分析的轨迹文件，\-n指定索引文件，使用它可以在分析时指定不同的组来分析，\-s指定  
拓扑文件，\-d z指定沿着z轴方向进行分析。__

__如果要指定分析索引组 1 的密度，可以使用命令管道：__

__echo 1 | gmx density \-f FILE\.trr \-n FILE\.ndx \-s FILE\.tpr \-d z \-o density\_1\.xvg__

__此程序不支持根据残基名称来获取密度，可通过gmx make\_ndx来获取索引组代号再通过命令管道传  
给gmx density实现。__

#### 6\.4\.18 gmx densmap

##### 概要

__gmx densmap \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-od \[<\.dat>\] \] \[ \-o \[<\.xpm>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-bin \] \[ \-aver \]  
\[ \-xmin \] \[ \-xmax \] \[ \-n1 \] \[ \-n2 \]  
\[ \-amax \] \[ \-rmax \] \[ \-\[no\]mirror \] \[ \-\[no\]sums \]  
\[ \-unit \] \[ \-dmin \] \[ \-dmax \]__

##### 说明

__gmx densmap用于计算2D数密度图。它可以计算平面和轴向\-径向密度图。输出的 \.xpm ↪ 620 文件可以  
使用例如xv等程序可视化，也可以使用xpm2ps 转换为postscript。此外，也可以使用\-od选项输出  
文本形式的 \.dat ↪ 608 文件，而不是输出通常由\-o 选项指定的 \.xpm ↪ 620 文件。__

__程序默认分析选定的一组原子在xy平面内的二维数密度图。可以使用 \-aver 选项改变进行平均的方  
向。如果设定了\-xmin和/或\-xmax，计算时只会考虑平均方向上处于限制范围之内的原子。可以使用  
\-bin选项设置格点间距。当\-n1或\-n2取非零值时，格点大小由此选项设定。计算时适当地考虑了  
盒子大小的波动。__

__如果设定了\-amax和\-rmax选项，会计算轴向\-径向数密度图。这种情况下应提供三个组，前两个组的  
质心定义轴线，第三个组为待分析的组。轴向范围从\-amax到\+amax，其中心为两质心的中点，并且正  
方向从第一组的质心到第二组的质心。默认径向范围从 0 到\+rmax，如果指定了\-mirror选项，则径  
向范围从\-rmax到\+rmax。__

__可以使用\-unit 选项对输出进行归一化。默认给出的是实际数密度。使用\-unit nm\-2 选项可以忽略  
对平均或角度方向的归一化。使用\-unit count选项可以得到每个格点单元的计数值。如果不希望输  
出中的刻度范围为从零到最大密度值，可以使用\-dmax选项设置最大密度值。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-od \[<\.dat>\] densmap\.dat 可选 通用数据文件__

__\-o \[<\.xpm>\] densmap\.xpm X PixMap兼容的矩阵文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0 只使用时刻之间的时间间隔（默认单位t除以dt的余数等于第一帧时间的帧，即分析时两帧ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-bin <real> 0\.02 格点尺寸（nm）__

__\-aver <enum> z 平均的方向：z，y，x__

__\-xmin <real> \-1 平均时的最小坐标__

__\-xmax <real> \-1 平均时的最大坐标__

__\-n1 \(^0\) 第一个方向的格点单元数  
\-n2 0 第二个方向的格点单元数  
\-amax 0 距离中心的最大轴向距离  
\-rmax 0 距离中心的最大径向距离  
\-\[no\]mirror no 在轴向轴下方添加镜像  
\-\[no\]sums no 将密度总和（1D图）输出到标准输出  
\-unit nm\-3 输出单位：nm\-3，nm\-2，count  
\-dmin 0 输出中的最小密度  
\-dmax 0 输出中的最大密度（ 0 表示由计算值决定）__

#### 6\.4\.19 gmx densorder

##### 概要

__gmx densorder \[ \-s \[<\.tpr>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.dat>\] \] \[ \-or \[<\.out> \[\.\.\.\]\] \] \[ \-og \[<\.xpm> \[\.\.\.\]\] \]  
\[ \-Spect \[<\.out> \[\.\.\.\]\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-\[no\]1d \] \[ \-bw \]  
\[ \-bwn \] \[ \-order \] \[ \-axis \]  
\[ \-method \] \[ \-d1 \] \[ \-d2 \]  
\[ \-tblock \] \[ \-nlevel \]__

##### 说明

__gmx densorder基于一段MD轨迹计算沿某一轴线的两相密度分布，并通过将其拟合为界面密度的函  
数曲线，得到随时间变化的 2 维表面波动。使用\-tavg选项可以输出界面的时间平均的空间表示。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.dat>\] Density4D\.dat 可选 通用数据文件__

__\-or \[<\.out> \[\.\.\.\]\] hello\.out 可选 通用输出文件__

__\-og \[<\.xpm> \[\.\.\.\]\] interface\.xpm 可选 X PixMap兼容的矩阵文件__

__\-Spect \[<\.out> \[\.\.\.\]\] intfspect\.out 可选 通用输出文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-\[no\]1d no 准 1 维界面几何结构__

__\-bw <real> 0\.2 平行于界面的密度分布的分格宽度__

__\-bwn <real> 0\.05 垂直于界面的密度分布的分格宽度__

__\-order \(^0\) 高斯滤波器的阶数， 0 阶等于不使用滤波  
\-axis Z 轴的方向，X，Y或Z  
\-method bisect 定位界面的方法：bisect，functional  
\-d1 0 相 1 的体相密度（小z值处）  
\-d2 \(^1000\) 相 2 的体相密度（大z值处）  
\-tblock \(^100\) 一个时间块平均所用的帧数  
\-nlevel \(^100\) 2D XPixMaps中的高度的水平数__

#### 6\.4\.20 gmx dielectric

##### 概要

__gmx dielectric \[ \-f \[<\.xvg>\] \] \[ \-d \[<\.xvg>\] \] \[ \-o \[<\.xvg>\] \] \[ \-c \[<\.xvg>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-\[no\]w \]  
\[ \-xvg \] \[ \-\[no\]x1 \] \[ \-eint \] \[ \-bfit \]  
\[ \-efit \] \[ \-tail \] \[ \-A \] \[ \-tau1 \]  
\[ \-tau2 \] \[ \-eps0 \] \[ \-epsRF \]  
\[ \-fix \] \[ \-ffn \] \[ \-nsmooth \]__

##### 说明

__gmx dielectric可以利用模拟得到的总偶极矩的自相关函数计算频率相关的介电常数。所需的自相关  
函数ACF可以使用 gmx dipoles ↪ 216 计算。可用的函数形式如下：__

- __单参数：y = exp\(\-a\_1 x\),__
- __双参数：y = a\_2 exp\(\-a\_1 x\),__
- __三参数：y = a\_2 exp\(\-a\_1 x\) \+ \(1 \- a\_2\) exp\(\-a\_3 x\)。__

__拟合过程的起始值可以在命令行中指定。也可以使用\-fix选项指定想要固定的参数的编号，这样参数  
就可以固定为它们的起始值。__

__程序会生成三个输出文件，第一个文件中包含了ACF，对ACF使用 1 ， 2 或 3 个参数的指数拟合，以  
及组合数据/拟合的数值导数。第二个文件包含了频率相关介电常数的实部和虚部，最后一个文件给出  
了所谓的Cole\-Cole图，图中的虚部是实部的函数。对于纯指数弛豫（Debye弛豫），Cole\-Cole图应该  
是半圆。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f__

__\[<\.xvg>\] dipcorr\.xvg xvgr/xmgr文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-d__

__\[<\.xvg>\] deriv\.xvg xvgr/xmgr文件__

__\-o__

__\[<\.xvg>\] epsw\.xvg xvgr/xmgr文件__

__\-c__

__\[<\.xvg>\] cole\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]x1 yes 使用第一列而不是第一个数据集作为 x 轴数据__

__\-eint <real> 5 结束对数据的积分并开始进行拟合的时间__

__\-bfit <real> 5 拟合的起始时间__

__\-efit \(^500\) 拟合的终止时间  
\-tail \(^500\) 函数的长度，包括数据和来自拟合的拖尾  
\-A 0\.5 拟合参数A的起始值  
\-tau1 10 拟合参数tau1的起始值  
\-tau2 1 拟合参数tau2的起始值  
\-eps0 80 液体的epsilon0  
\-epsRF 78\.5 模拟中使用的反应场的介电常数值。 0 意味着无穷大。  
\-fix \(^0\) 将参数固定为其起始值，A（ 2 ），tau1（ 1 ）或tau2（ 4 ）  
\-ffn none  
拟合函数类型：none，exp，aexp，exp\_exp，exp5，  
exp7，exp9  
\-nsmooth 3 用于平滑的点数__

#### 6\.4\.21 gmx dipoles

##### 概要

__gmx dipoles \[ \-en \[<\.edr>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \]__

__\[ \-n \[<\.ndx>\] \] \[ \-o \[<\.xvg>\] \] \[ \-eps \[<\.xvg>\] \] \[ \-a \[<\.xvg>\] \]__

__\[ \-d \[<\.xvg>\] \] \[ \-c \[<\.xvg>\] \] \[ \-g \[<\.xvg>\] \]__

__\[ \-adip \[<\.xvg>\] \] \[ \-dip3d \[<\.xvg>\] \] \[ \-cos \[<\.xvg>\] \]__

__\[ \-cmap \[<\.xpm>\] \] \[ \-slab \[<\.xvg>\] \] \[ \-b <time> \] \[ \-e <time> \]__

__\[ \-dt <time> \] \[ \-\[no\]w \] \[ \-xvg <enum> \] \[ \-mu <real> \]__

__\[ \-mumax <real> \] \[ \-epsilonRF <real> \] \[ \-skip <int> \]__

__\[ \-temp <real> \] \[ \-corr <enum> \] \[ \-\[no\]pairs \] \[ \-\[no\]quad \]__

__\[ \-ncos <int> \] \[ \-axis <string> \] \[ \-sl <int> \]__

__\[ \-gkratom <int> \] \[ \-gkratom2 <int> \] \[ \-rcmax <real> \]__

__\[ \-\[no\]phi \] \[ \-nlevels <int> \] \[ \-ndegrees <int> \]__

__\[ \-acflen <int> \] \[ \-\[no\]normalize \] \[ \-P <enum> \]__

__\[ \-fitfn <enum> \] \[ \-beginfit <real> \] \[ \-endfit <real> \]__

##### 说明

__gmx dipoles用于计算模拟系统的总偶极矩及其波动。利用这些数据你可以计算其他一些性质，例如低  
介电介质的介电常数。对于具有净电荷的分子，会在分子的质心处减去分子的净电荷。  
输出文件Mtot\.xvg中包含了每帧的总偶极矩，总偶极矩的分量及其大小。输出文件 aver\.xvg中包含  
了模拟过程中的<|mu|^2>和||^2。输出文件dipdist\.xvg中包含了模拟过程中偶极矩的分布。  
可以使用\-mumax选项来指定分布图的最高值。  
此外，如果指定了\-corr选项，程序会计算偶极自相关函数。输出文件的名称可通过\-c选项指定。相  
关函数可以是所有分子（mol）的平均值，每个分子的单独值（molsep），或者根据模拟盒子总偶极矩  
（total）计算的值。__

__使用 \-g选项可以计算Kirkwood G因子与距离的关系，以及偶极夹角余弦的平均值与距离的函数关__

__系。图中也包括了gOO和hOO，具体方法可参考Nymand & Linse, J\. Chem\. Phys\. 112 \(2000\) pp__

__6386\-6395。在同一图中，还包括了每一尺度的能量，它是偶极内积与距离三次方的比值。__

##### 示例

__gmx dipoles \-corr mol \-P 1 \-o dip\_sqr \-mu 2\.273 \-mumax 5\.0  
上面的命令会计算分子偶极矩的自相关函数，计算时使用偶极矩向量与其t时刻后的值之间的夹角的一  
阶Legendre多项式。此计算会使用 1001 帧。此外，还计算 \-epsilonRF无穷大（默认），温度300 K  
（默认），分子平均偶极矩2\.273（SPC）条件下的介电常数。对分布函数，其最大值指定为5\.0。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-en \[<\.edr>\] ener\.edr 可选 能量文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] Mtot\.xvg xvgr/xmgr文件__

__\-eps \[<\.xvg>\] epsilon\.xvg xvgr/xmgr文件__

__\-a \[<\.xvg>\] aver\.xvg xvgr/xmgr文件__

__\-d \[<\.xvg>\] dipdist\.xvg xvgr/xmgr文件__

__\-c \[<\.xvg>\] dipcorr\.xvg 可选 xvgr/xmgr文件__

__\-g \[<\.xvg>\] gkr\.xvg 可选 xvgr/xmgr文件__

__\-adip \[<\.xvg>\] adip\.xvg 可选 xvgr/xmgr文件__

__\-dip3d__

__\[<\.xvg>\] dip3d\.xvg 可选 xvgr/xmgr文件__

__\-cos \[<\.xvg>\] cosaver\.xvg 可选 xvgr/xmgr文件__

__\-cmap \[<\.xpm>\] cmap\.xpm 可选 X PixMap兼容的矩阵文件__

__\-slab \[<\.xvg>\] slab\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

读入轨迹最后一帧的时间，即分析的结束时间（默认单位

__ps）__

__\-dt <time> 0 只使用时刻时两帧之间的时间间隔（默认单位t除以dt的余数等于第一帧时间的帧，即分析ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-mu <real> \-1 单个分子的偶极矩（单位：德拜）__

__\-mumax <real> 5 以德拜为单位的最大偶极矩（用于直方图）__

__\-epsilonRF__

__<real>^0__

__模拟中使用的反应场的epsilon值，用于计算介电常数。警__

__告：0\.0代表无穷大（默认）__

__\-skip \(^0\) 输出结果中忽略的步数（但计算时使用了所有步）  
\-temp \(^300\) 模拟的平均温度（用于计算介电常数）  
\-corr none 要计算的相关函数：none，mol，molsep，total  
\-\[no\]pairs yes 计算所有分子对之间的|cos\(theta\)|。可能会很慢  
\-\[no\]quad no 考虑四极矩  
\-ncos 1__

只能为 1 或 2 。决定了是计算同一组中的所有分子之间的

__<cos\(theta\)>，还计算来自两个不同组中的分子之间的__

__<cos\(theta\)>。使用此选项会启用\-g选项。__

__\-axis <string> Z 计算盒子的法线沿X，Y或Z方向__

__\-sl <int> 10 将盒子划分为指定数目的切片。__

__\-gkratom <int> 0__

__计算距离依赖的Kirkwood因子时，使用分子的第n个原__

__子（从 1 开始）计算分子之间的距离，而不使用电荷中心__

__（选项为 0 时）__

__\-gkratom2 <int> 0 与上一选项相同，但用于ncos = 2的情况，即两组分子间__

__的偶极相互作用__

__\-rcmax <real> 0 偶极取向分布中使用的最大距离（用于如果为 0 ，会使用基于盒子长度的标准。ncos = 2的情况）。__

__\-\[no\]phi no__

__将扭转角度输出到由\-cmap 选项指定的 \.xpm ↪ 620 文件中，__

__扭转角度定义为两个分子的偶极向量绕分子间距离向量的旋__

__转角度。默认给出的是偶极矩夹角的余弦值。__

__\-nlevels <int> 20 输出颜色映射图中颜色的数目__

__\-ndegrees <int> 90 输出颜色映射图中 y 轴的划分数（用于 180 度）__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0 用于ACF的Legendre多项式的阶数（^0 表示不使用）:__

__0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit \(^0\) 对相关函数进行指数拟合的起始时间  
\-endfit \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

#### 6\.4\.22 gmx disre

##### 概要

__gmx disre \[ \-s \[<\.tpr>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]__

__\[ \-c \[<\.ndx>\] \] \[ \-ds \[<\.xvg>\] \] \[ \-da \[<\.xvg>\] \] \[ \-dn \[<\.xvg>\] \]__

__\[ \-dm \[<\.xvg>\] \] \[ \-dr \[<\.xvg>\] \] \[ \-l \[<\.log>\] \] \[ \-q \[<\.pdb>\] \]__

__\[ \-x \[<\.xpm>\] \] \[ \-b <time> \] \[ \-e <time> \] \[ \-dt <time> \] \[ \-\[no\]w \]__

__\[ \-xvg <enum> \] \[ \-ntop <int> \] \[ \-maxdr <real> \]__

__\[ \-nlevels <int> \] \[ \-\[no\]third \]__

##### 说明

__gmx disre用于计算对距离限制的违反情况。程序总是计算瞬时违反情况而不是时间平均的违反情况，  
因为分析是后来根据轨迹文件完成的，使用时间平均没有意义。尽管如此，每个限制的时间平均值还是  
会输出到日志文件中。__

__要输出选中的特定限制，可以使用索引文件中的索引组标签。__

__当指定可选的\-q选项时，会输出一个 \.pdb ↪ 614 文件，并使用平均违反量对其着色。__

__当指定\-c 选项时，程序会读取一个索引文件，其中包含了轨迹中与待分析的团簇（以其他方式定义）  
对应的的帧。对于这些团簇，程序会使用三次平均算法计算平均违反情况，并将其输出到日志文件中。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 轨迹文件： gro xtc ↪^621 ， trr ↪^619 ， cpt ↪^608 ，__

__↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] viol\.ndx 可选 索引文件__

__\-c \[<\.ndx>\] clust\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ds \[<\.xvg>\] drsum\.xvg xvgr/xmgr文件__

__\-da \[<\.xvg>\] draver\.xvg xvgr/xmgr文件__

__\-dn \[<\.xvg>\] drnum\.xvg xvgr/xmgr文件__

__\-dm \[<\.xvg>\] drmax\.xvg xvgr/xmgr文件__

__\-dr \[<\.xvg>\] restr\.xvg xvgr/xmgr文件__

__\-l \[<\.log>\] disres\.log 日志文件__

__\-q \[<\.pdb>\] viol\.pdb 可选 蛋白质数据库文件__

__\-x \[<\.xpm>\] matrix\.xpm 可选 X PixMap兼容的矩阵文件__

##### 控制选项

##### 选项 默认值 说明

##### 6\.4\. 命令说明 219

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-ntop \(^0\) 每一步存储在日志文件中的较大违反的次数  
\-maxdr 0__

输出矩阵中最大的距离违反。此值如果小于或等于 0 ，将根据

数据确定最大值。

__\-nlevels \(^20\) 输出矩阵的水平数  
\-\[no\]third yes 对输出矩阵使用三次反比平均或线性平均__

#### 6\.4\.23 gmx distance

##### 概要

__gmx distance \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-oav \[<\.xvg>\] \] \[ \-oall \[<\.xvg>\] \] \[ \-oxyz \[<\.xvg>\] \]  
\[ \-oh \[<\.xvg>\] \] \[ \-oallstat \[<\.xvg>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-tu \]  
\[ \-fgroup \] \[ \-xvg \] \[ \-\[no\]rmpbc \]  
\[ \-\[no\]pbc \] \[ \-sf \] \[ \-selrpos \]  
\[ \-seltype \] \[ \-select \] \[ \-len \]  
\[ \-tol \] \[ \-binw \]__

##### 说明

__gmx distance用于计算一对位置之间的距离和时间的函数关系。每个选区指定要计算的一组单独距离。  
每个选区应由位置对组成，计算的距离为位置1\-2，3\-4等之间的距离。__

__\-oav选项指定的输出文件中为每个选区的平均距离对时间的函数。\-oall选项指定的输出文件中为所  
有单独的距离对时间的函数。\-oxyz选项指定的输出文件中也是所有单独的距离对时间的函数，但包含  
的是距离的x，y和z分量，而不是距离的大小。\-oh选项指定的输出文件中为每个选区的距离的直方  
图。直方图的位置由\-len和\-tol指定。分格宽度由\-binw指定。\-allallst选项指定的输出文件  
中为对帧进行平均的每个单独距离的平均值和标准差。__

__注意，gmx distance计算的距离是固定对（1\-2，3\-4等）之间的，这些固定对由单个选区指定。要计  
算两个选区之间的距离，包括最小值，最大值和成对距离，请使用 gmx pairdist ↪ 295 。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选__

__输入结构： tpr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-oav \[<\.xvg>\] distave\.xvg 可选 平均距离对时间的函数__

__\-oall \[<\.xvg>\] dist\.xvg 可选 所有距离对时间的函数__

__\-oxyz \[<\.xvg>\] distxyz\.xvg 可选 距离分量对时间的函数__

__\-oh \[<\.xvg>\] disthist\.xvg 可选 距离的直方图__

__\-oallstat \[<\.xvg>\] diststat\.xvg 可选 各个距离的统计数据__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

读入轨迹第一帧的时间，即分析的起始时间（默认单位

__ps）__

__\-e <time> 0__

读入轨迹最后一帧的时间，即分析的终止时间（默认单位

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分__

__析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

轨迹文件中存储的原子（如果未设置，假定为前N个原

子）

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，whole\_mol\_cog，__

__part\_res\_com，part\_res\_cog，part\_mol\_com，__

__part\_mol\_cog，dyn\_res\_com，dyn\_res\_cog，__

__dyn\_mol\_com，dyn\_mol\_cog__

__\-select__

__<selection> 要计算距离的位置对__

__\-len <real> 0\.1 直方图的平均距离__

__\-tol <real> 1 整个分布的宽度，为\-len的比例__

__\-binw <real> 0\.001 直方图的分格宽度__

#### 6\.4\.24 gmx dos

##### 概要

__gmx dos \[ \-f \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-vacf \[<\.xvg>\] \] \[ \-mvacf \[<\.xvg>\] \] \[ \-dos \[<\.xvg>\] \]  
\[ \-g \[<\.log>\] \] \[ \-b \] \[ \-e \] \[ \-dt \] \[ \-\[no\]w \]  
\[ \-xvg \] \[ \-\[no\]v \] \[ \-\[no\]recip \] \[ \-\[no\]abs \] \[ \-\[no\]normdos \]  
\[ \-T \] \[ \-toler \] \[ \-acflen \] \[ \-\[no\]normalize \]  
\[ \-P \] \[ \-fitfn \] \[ \-beginfit \]  
\[ \-endfit \]__

##### 说明

__gmx dos根据模拟计算态密度（Density of States）。为保证计算有意义，必须以足够高的频率来保存轨  
迹中的速度，这样才能覆盖所有的振动。对柔性系统，保存轨迹的时间间隔大约是几个fs。程序会将基  
于DoS的性质输出到标准输出。注意，态密度是根据质量加权的自相关计算的，默认只使用实部的平方  
而不使用绝对值。这意味着所得的形状与使用gmx velacc 计算的普通振动功率谱大不相同。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.trr/\.cpt/\.\.\.>\] traj\.trr 全精度轨迹文件： trr ↪ 619 ， cpt ↪ 608 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-vacf \[<\.xvg>\] vacf\.xvg xvgr/xmgr文件__

__\-mvacf__

__\[<\.xvg>\] mvacf\.xvg xvgr/xmgr文件__

__\-dos \[<\.xvg>\] dos\.xvg xvgr/xmgr文件__

__\-g \[<\.log>\] dos\.log 日志文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]v yes 显示更多信息__

__\-\[no\]recip no DoS图的X轴使用cm^\-1而不是1/ps。__

__\-\[no\]abs no__

__使用VACF傅里叶变换的绝对值作为态密度。默认仅仅使__

__用实部__

__\-\[no\]normdos no 归一化DoS，以便使其总和等于3N。通常并不需要这样做。__

__\-T <real> 298\.15 模拟温度__

__\-toler <real> 1e\-06 \[隐藏选项\]使用二分法计算流动性时的容差__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0__

__用于ACF的Legendre多项式的阶数（ 0 表示不使用）:__

__0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit <real> 0 对相关函数进行指数拟合的起始时间__

__\-endfit <real> \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

##### 已知问题

##### • 此程序运行时需要大量内存：总使用量等于原子数乘以 3 乘以帧数再乘以 4 （或 8 ，如果使用双精

##### 度）。

#### 6\.4\.25 gmx dssp\(2023\)

##### 概要

__gmx dssp \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.dat>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-tu \] \[ \-fgroup \] \[ \-xvg \]  
\[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \] \[ \-selrpos \]  
\[ \-seltype \] \[ \-sel \] \[ \-hmode \]  
\[ \-\[no\]nb \] \[ \-cutoff \] \[ \-\[no\]pihelix \]  
\[ \-ppstretch \]__

##### 说明

__gmx dssp可以使用DSSP算法（即通过检测氨基酸残基之间氢键的特定模式）来确定蛋白质的二级结  
构。__

__\-hmode用于指定氢原子的来源,直接使用结构中的氢原子（gromacs选项）,还是根据前一个残基的C  
原子和O原子坐标计算氢的赝原子（dssp选项）。__

__\-nb可以使用GROMACS的邻区搜索方法来查找可能存在氢键的残基对，而不是简单地遍历残基查找  
它们自身之间存在的氢键。__

__\-cutoff为一个实数值，定义了残基与其邻近残基之间的最大距离，与\-nb选项配合使用。最小值（也  
是推荐值）为0\.9。__

__\-pihelix更改模式搜索算法，使其更偏向于pi螺旋。__

__\-ppstretch定义聚脯氨酸螺旋的拉伸值。shortened表示拉伸值为 2 ，default表示拉伸值为 3 。__

__注意，如果蛋白质的结构是使用X射线晶体学以外的方法确定的（\.pdb格式的结构中, CRYST1行中  
的值不正确），由于结构的晶胞大小不正确,目前gmx dssp无法重现它的二级结构。__

__注意，无论GROMACS的配置精度如何，计算始终以单精度进行。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型: xtctrrcptgrog96__

__pdbtng__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构: tprgrog96pdb brk ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.dat>\] dssp\.dat DSSP输出文件的名称__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时间（默认单位__

__ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0 只使用时刻析时两帧之间的时间间隔（默认单位t除以dt的余数等于第一帧时间的帧，即分ps）__

__\-tu <enum> ps 时间值的单位: fs, ps, ns, us, ms, s__

__\-fgroup__

__<selection> 轨迹文件中存储的原子\(若未设定,则假定为前N个原子\)__

__\-xvg <enum> xmgrace 绘图格式: xmgrace, xmgr, none__

__\-\[no\]rmpbc yes 保证每一帧的分子都完整__

__\-\[no\]pbc yes 计算距离时应用周期性边界条件__

__\-sf <file> 使用文件提供选区__

__\-selrpos <enum> atom__

__选区参考位置: atom, res\_com, res\_cog, mol\_com,__

__mol\_cog, whole\_res\_com, whole\_res\_cog,__

__whole\_mol\_com, whole\_mol\_cog, part\_res\_com,__

__part\_res\_cog, part\_mol\_com, part\_mol\_cog,__

__dyn\_res\_com, dyn\_res\_cog, dyn\_mol\_com,__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置: atom, res\_com, res\_cog, mol\_com,__

__mol\_cog, whole\_res\_com, whole\_res\_cog,__

__whole\_mol\_com, whole\_mol\_cog, part\_res\_com,__

__part\_res\_cog, part\_mol\_com, part\_mol\_cog,__

__dyn\_res\_com, dyn\_res\_cog, dyn\_mol\_com,__

__dyn\_mol\_cog__

__\-sel <selection> DSSP索引组__

__\-hmode <enum> gromacs 氢赝原子生成模式: gromacs, dssp__

__\-\[no\]nb yes 使用GROMACS邻区搜索方法__

__\-cutoff <real> 0\.9 邻区搜索中,残基与其邻近残基的截断距离\.必须>= 0\.9__

__\-\[no\]pihelix no 优先考虑Pi螺旋__

__\-ppstretch <enum> default PP螺旋的伸缩值: shortened, default__

#### 6\.4\.26 gmx do\_dssp\(2019\)

##### 概要

__gmx do\_dssp \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-map \[<\.map>\] \] \[ \-ssdump \[<\.dat>\] \] \[ \-o \[<\.xpm>\] \]  
\[ \-sc \[<\.xvg>\] \] \[ \-a \[<\.xpm>\] \] \[ \-ta \[<\.xvg>\] \]  
\[ \-aa \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]__

__\[ \-tu <enum> \] \[ \-\[no\]w \] \[ \-xvg <enum> \] \[ \-sss <string> \]__

__\[ \-ver <int> \]__

##### 说明

__gmx do\_dssp读取轨迹文件，并调用第三方程序dssp计算每一时间帧蛋白的二级结构。如果你尚未安  
装dssp程序，请到http://swift\.cmbi\.ru\.nl/gv/dssp下载安装。gmx do\_dssp假定dssp可执行文件的  
路径为/usr/local/bin/dssp。否则，需要设置一个环境变量DSSP，其值为dssp可执行文件的完整  
路径，例如在csh中可以使用：  
setenv DSSP /opt/dssp/bin/dssp。如果使用bash，可以使用export DSSP='/opt/dssp/bin/dssp'，  
也可以直接将该变量添加到bash的配置文件\.bashrc中。  
从2\.0\.0版本起，dssp的语法与早期版本有所不同。如果你正在使用旧版本的dssp，可指定\-ver选项  
保证do\_dssp使用旧版本的语法。默认情况下，do\_dssp使用2\.0\.0版引入的语法。此外，程序假定更  
新版本的dssp（编写此文档时尚未发布）也使用与2\.0\.0版本相同的语法。  
程序会将每个残基每一时间帧的二级结构信息输出到一个 \.xpm ↪ 620 矩阵文件。此文件是一个文本文件，  
可以用文本编辑器打开查看，其中用不同字符表示蛋白质每一残基所属的二级结构，并随时间变化，同  
时还定义了每个字符的颜色。也可以用 xv 之类的程序可视化这个文件，还可以使用gmx xpm2ps命  
令将这个文件转换为postscript格式，以便插入到LaTex文件中。在 \.xpm ↪ 620 和postscript文件中，蛋  
白的每条链以浅灰色线分隔开。程序可以统计每个二级结构类型的残基数目以及二级结构类型的总数  
（\-sss），并将其与时间的函数输出到文件（\-sc）。输出文件中包含了所有不同二级结构的残基数目，  
可以使用xmgrace的\-nxy选项打开查看。  
程序可以计算每个残基的溶剂可及表面积（SAS），包括绝对值（A^2）和相对于残基最大可及表面积的  
比例。残基的最大可及表面积定义为该残基在甘氨酸链中的可及表面积。注意， gmx sasa ↪ 320 程序也可  
用于计算SAS，且效率更高。  
最后，这个程序可以将二级结构转存到一个特殊文件ssdump\.dat （此文件为文本文件，其中以字符表  
示残基的二级结构类型，如H代表螺旋，B代表折叠等）中，以供 gmx chi ↪ 194 程序使用。将这两个程  
序结合起来，就可以分析残基二面角性质与二级结构类型的函数关系。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 轨迹文件： gro xtc ↪^621 ， trr ↪^619 ， cpt ↪^608 ，__

__↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-map \[<\.map>\] ss\.map 库__

##### 指定矩阵数据映射到颜色的文件。程序输

__出\.xpm文件的原色库文件，如无则默认输__

__出。__

__输出文件选项__

__选项 默认文件 类型 说明__

__\-ssdump \[<\.dat>\] ssdump\.dat 可选 通用数据文件__

__\-o \[<\.xpm>\] ss\.xpm X PixMap兼容的矩阵文件__

__\-sc \[<\.xvg>\] scount\.xvg xvgr/xmgr文件__

__\-a \[<\.xpm>\] area\.xpm 可选 X PixMap兼容的矩阵文件__

__\-ta \[<\.xvg>\] totarea\.xvg 可选 xvgr/xmgr文件__

__\-aa \[<\.xvg>\] averarea\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两__

__帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-sss__

__<string> HEBT 对结构的二级结构类型进行计数__

__\-ver <int> 2 DSSP主版本号。自2\.0版本起语法有所改变__

#### 6\.4\.26 gmx dump

##### 概要

__gmx dump \[ \-s <\.tpr> \] \[ \-f <\.xtc/\.trr/\.\.\.> \] \[ \-e <\.edr> \] \[ \-cp <\.cpt> \]  
\[ \-p <\.top> \] \[ \-mtx <\.mtx> \] \[ \-om <\.mdp> \] \[ \-\[no\]nr \]  
\[ \-\[no\]param \] \[ \-\[no\]sys \] \[ \-\[no\]orgir \]__

##### 说明

__gmx dump读取一个运行输入文件（ \.tpr ↪ 619 ），轨迹文件（ \.trr ↪ 619 / \.xtc ↪ 621 /tng），能量文件（ \.edr ↪ 609 ）  
,检查点文件（ \.cpt ↪ 608 ）或拓扑文件\( \.top \)，而后将其以可读格式输出到标准输出。如果运行出现了问  
题，可以使用此程序检查运行输入文件。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 可选 运行输入文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-e \[<\.edr>\] ener\.edr 可选 能量文件__

__\-cp \[<\.cpt>\] state\.cpt 可选 检查点文件__

__\-p \[<\.top>\] topol\.top 可选 拓扑文件__

__\-mtx \[<\.mtx>\] hessian\.mtx 可选 Hessian矩阵__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-om \[<\.mdp>\] grompp\.mdp 可选 来自运行输入文件的grompp输入文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]nr yes 在输出中显示索引号（忽略它们更容易进行比较，但创建的拓扑无法__

__使用）__

__\-\[no\]param no 显示每一成键相互作用的参数（在比较时，与\-nonr选项结合使用__

__更好）__

__\-\[no\]sys no 列出整个系统的原子和成键相互作用，而不是列出每种分子类型的原__

__子和成键相互作用__

__\-\[no\]orgir no 显示来自tpr文件的输入参数，版本由生成文件的版本决定，而不使__

__用当前的版本__

##### 已知问题

- __grompp无法读取\-om选项产生的 \.mdp 文件\.__

#### 6\.4\.27 gmx dyecoupl

##### 概要

__gmx dyecoupl \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-ot \[<\.xvg>\] \]  
\[ \-oe \[<\.xvg>\] \] \[ \-o \[<\.dat>\] \] \[ \-rhist \[<\.xvg>\] \]  
\[ \-khist \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-tu \]  
\[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]pbcdist \] \[ \-\[no\]norm \]  
\[ \-bins \] \[ \-R0 \]__

##### 说明

__gmx dyecoupl用于从轨迹文件中提取染料动力学。目前，可提取染料分子间的R和kappa^2用于  
\(F\)RET模拟，并假定偶极耦合遵从Foerster方程。此外，程序还可以计算R\(t\)和kappa^2\(t\)，R和  
kappa^2的直方图和平均值，以及对应Foerster半径R\_0（\-R0选项）的瞬时FRET效率E\(t\)。输入  
染料分子必须是完整的（参见trjconvpbc选项的res，mol）。染料分子的跃迁偶极矩至少要使用一  
对原子进行定义，但也可以使用索引文件提供的多个原子对。距离R基于给定原子对的质心进行计算。  
如果指定了\-pbcdist选项，程序会计算到最近的周期映像的距离，而不是盒子内的距离。但这只适用  
于具有 3 维周期性边界的情况。\-norm选项可用于对直方图进行（面积）归一化。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ot \[<\.xvg>\] rkappa\.xvg 可选 xvgr/xmgr文件__

__\-oe \[<\.xvg>\] insteff\.xvg 可选 xvgr/xmgr文件__

__\-o \[<\.dat>\] rkappa\.dat 可选 通用数据文件__

__\-rhist__

__\[<\.xvg>\] rhist\.xvg 可选 xvgr/xmgr文件__

__\-khist__

__\[<\.xvg>\] khist\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]pbcdist no 计算距离R时使用PBC__

__\-\[no\]norm no 归一化直方图__

__\-bins \(^50\) 直方图的分格数  
\-R0 \-1 包含kappa^2=2/3的Foerster半径，单位nm__

#### 6\.4\.28 gmx dyndom\(2019\)

##### 概要

__gmx dyndom \[ \-f \[<\.pdb>\] \] \[ \-n \[<\.ndx>\] \] \[ \-o \[<\.xtc/\.trr/\.\.\.>\] \]  
\[ \-firstangle \] \[ \-lastangle \] \[ \-nframe \]  
\[ \-maxangle \] \[ \-trans \] \[ \-head \]  
\[ \-tail \]__

##### 说明

__gmx dyndom读取DynDom程序（http://www\.cmp\.uea\.ac\.uk/dyndom/）输出的 \.pdb ↪ 614 文件。它会读  
取坐标，旋转轴的坐标以及包含分区的索引文件。此外，它将向量文件的第一个和最后一个原子作为命  
令行参数（\-head 和\-tail 选项），并最终得到转换向量（在DynDom的info文件中给出）和旋转角  
度（也作为命令行参数）。如果给出了由DynDom确定的角度，你应该能够恢复用于生成DynDom输  
出文件的二级结构。由于数值精度有限，应该通过计算所有原子的RMSD（使用 gmx confrms ↪ 202 ）而不  
是通过对比文件（使用diff）来进行验证。__

__本程序的目的是对DynDom发现的旋转进行插值和外推。因此，可能会产生含有过长或过短键，或存  
在重叠原子的非真实结构。你可能需要查看并进行能量最小化以验证结构。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f__

__\[<\.pdb>\] dyndom\.pdb 蛋白质数据库文件__

__\-n__

__\[<\.ndx>\] domains\.ndx 索引文件__

__输出文件选项__

__选项 默认文件 类型 说明__

__\-o \[<\.xtc/\.trr/\.\.\.>\] rotated\.xtc__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ， tng ↪ 617__

##### 控制选项

##### 选项 默认值 说明

__\-firstangle \(^0\) 绕旋转向量的旋转角度  
\-lastangle \(^0\) 绕旋转向量的旋转角度  
\-nframe 11 路径上的步数  
\-maxangle 0 DymDom确定的绕旋转向量的旋转角度  
\-trans 0 沿旋转向量的平移量（单位：埃）（参见DynDom的info  
文件）  
\-head 0 0 0 箭头向量的第一个原子  
\-tail 0 0 0 箭头向量的最后一个原子__

#### 6\.4\.29 gmx editconf

##### 概要

__gmx editconf \[ \-f \[<\.gro/\.g96/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-bf \[<\.dat>\] \]  
\[ \-o \[<\.gro/\.g96/\.\.\.>\] \] \[ \-mead \[<\.pqr>\] \] \[ \-\[no\]w \]  
\[ \-\[no\]ndef \] \[ \-bt \] \[ \-box \]  
\[ \-angles \] \[ \-d \] \[ \-\[no\]c \]  
\[ \-center \] \[ \-aligncenter \]  
\[ \-align \] \[ \-translate \]  
\[ \-rotate \] \[ \-\[no\]princ \] \[ \-scale \]  
\[ \-density \] \[ \-\[no\]pbc \] \[ \-resnr \] \[ \-\[no\]grasp \]  
\[ \-rvdw \] \[ \-\[no\]sig56 \] \[ \-\[no\]vdwread \] \[ \-\[no\]atom \]  
\[ \-\[no\]legend \] \[ \-label \] \[ \-\[no\]conect \]__

##### 说明

__gmx editconf的主要功能是对系统的结构进行编辑，也可以将通用结构格式保存或转换为 \.gro ↪ 610 ，  
\.g96 ↪ 609 或 \.pdb ↪ 614 等其他格式。__

__在分子动力学模拟中，通常要将系统放到一个周期性的盒子中，gmx editconf有许多控制盒子的选项。  
可以使用\-box，\-d和\-angles选项修改盒子。除非指定了\-noc选项，否则\-box和\-d选项都会  
将系统在盒子内居中。可以使用 \-center选项将系统的几何中心从\-c 选项隐含的默认值\(x/2, y/2,  
z/2\)移动到其他位置。__

__选项\-bt指定盒子类型：triclinic为三斜盒子，cubic为所有边长都相等的长方体盒子（即立方盒  
子），dodecahedron代表菱形十二面体盒子（等边十二面体），octahedron 为截角八面体盒子（将两  
个底面重合的四面体切去方向相反的两端，同时保证所有边长相等）。后两种盒子是三斜盒子的特例。截  
角八面体三个盒向量的长度为两个相对的六边形之间的最短距离。与具有周期性映像距离的立方盒子相  
比，具有相同周期距离的菱形十二面体盒子的体积是立方盒子的71%，而截角八面体盒子的体积是立方  
盒子的77%。__

__对一般的三斜盒子，\-box选项需要指定盒子的三个边长，对立方盒子，菱形十二面体盒子，或截角八  
面体盒子，\-box选项只需要指定一个值，即盒子的边长。__

__\-d选项指定系统中的原子到盒子边界的最小距离。对三斜盒子会使用系统在 x ， y 和 z 分方向的大小来  
确定距离。对立方盒子，菱形十二面体盒子或截角八面体盒子，盒子的大小被设置为系统的直径（原子  
间的最大距离）加上两倍的指定距离。__

__\-angles选项只能与\-box选项和三斜盒子一起使用才有意义，而且不能与\-d 选项一起使用。__

__如果指定了 \-n或\-ndef 选项，可以从指定的索引文件中选择一个组来计算大小和几何中心，否则会  
使用整个系统的大小和几何中心。__

__可以使用 \-rotate选项旋转坐标和速度。如\-rotate 0 30 0 会将系统绕Y轴沿顺时针方向旋转 30  
度。__

__可以使用 \-princ选项将系统（或系统的某一部分）的主轴与坐标轴平齐，并且最长的轴沿 x 轴方向。  
这可以减小盒子的体积，特别是当分子为长条形时。但要注意分子在纳秒的时间尺度内可能会发生明显  
的旋转，所以使用时要小心。__

__缩放会在任何其他操作之前进行。可以对盒子和坐标进行缩放使密度达到指定值（\-density选项）。注  
意，如果输入为 \.gro ↪ 610 文件，这种做法可能不准确。\-scale选项的一个特殊功能是，当某一维度的缩  
放因子为\-1时，可得到系统关于相关平面的镜像。当三个维度的缩放因子都为\-1时，可得到系统关于坐  
标原点的镜像。__

__组的选择是在所有其他操作都完成之后进行的。在输出时，可以只输出系统中的某一个组，或某一个部  
分，还可以建立划分更细致的索引文件，以便进行更加细致的选择输出。__

__可以粗略地去除系统的周期性。当去除周期性时，输入文件最底部的盒向量必须保证正确，这非常重要，  
因为gmx editconf去除周期性的算法十分简单，只是将原子坐标直接减去盒子边长。__

__当输出 \.pdb ↪ 614 文件时，可以使用\-bf选项添加B因子。B因子可以从文件中读取，格式如下：第一行  
声明文件所含B因子数值的个数，从第二行开始，每行声明一个索引号，后面跟着B因子。默认情况  
下，B因子会附加到每个残基上，每个残基的所有原子具有相同的数值，除非B因子数大于残基数或指  
定了\-atom 选项。显然，可以添加任何类型的数值数据而不仅仅是B因子。使用\-legend选项可以  
生成一系列CA原子，其B因子的范围为所用数据的最小值到最大值，它们可以有效地作为查看的图  
例，便于可视化软件显示。__

__使用 \-mead 选项可以生成一个特殊的 \.pdb ↪ 614 文件（\.pqr），它可用于MEAD静电程序（Poisson\-  
Boltzmann求解器）。使用这个选项的前提条件是输入文件必须为运行输入文件，因为这种文件中才包  
含了需要的参数。输出文件中的B因子字段为原子的范德华半径，占有率字段为原子的电荷。__

__\-grasp选项的作用与上一选项类似，只不过互换了电荷和半径的位置，电荷位于B因子字段，而半径  
位于占有率字段。__

__使用\-align选项可以将特定组的主轴与指定的向量平齐，同时\-aligncenter选项可以指定可选的旋  
转中心。__

__最后，使用 \-label选项，gmx editconf可以为 \.pdb ↪ 614 文件添加链标识符。如果一个文件中的不同  
残基属于不同的肽链，那么此选项可用于为残基指定肽链归属，这样不但有利于可视化，在使用一些程  
序如Rasmol进行分析时也很有帮助，在建立模拟体系时也更方便。__

__一些软件包（如GROMOS）在生成截角八面体时会使用切除立方体盒子边角的方法，为转换这种截角  
八面体文件，可使用：__

__gmx editconf\-f in \- rotate 045 35\.264\-bt o\-box veclen\-o out__

__其中veclen为立方盒子的边长乘以sqrt\(3\)/2。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.gro/\.g96/\.\.\.>\] conf\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp tpr ↪ 619__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-bf \[<\.dat>\] bfact\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.gro/\.g96/\.\.\.>\] out\.gro 可选 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp__

__\-mead \[<\.pqr>\] mead\.pqr 可选 用于MEAD的坐标文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no__

__查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614__

__文件__

__\-\[no\]ndef no 从默认索引组中选择输出__

__\-bt <enum> triclinic 用于cubic\-box，dodecahedron和\-d 的盒子类型：，octahedrontriclinic，__

__\-box <vector> 0 0 0 盒向量长度\(a, b, c\)__

__\-angles <vector> 90 90 90 盒向量之间的角度\(bc, ac, ab\)__

__\-d <real> 0 溶质分子与盒子边界间的距离__

__\-\[no\]c no__

__将分子在盒子内居中（\-box和\-d选项暗含此选__

__项）__

__\-center <vector> 0 0 0 将几何中心移到指定的\(x, y, z\)__

__\-aligncenter__

__<vector> 0 0 0 平齐时的旋转中心__

__\-align <vector> 0 0 0 要平齐的目标向量__

__\-translate <vector> 0 0 0 平移向量__

__\-rotate <vector> 0 0 0 绕X，Y和Z轴的旋转角度（以度为单位）__

__\-\[no\]princ no 使分子取向沿其主轴__

__\-scale <vector> 1 1 1 缩放因子__

__\-density <real> 1000 通过缩放使输出盒子的密度为指定值（g/L）__

__\-\[no\]pbc no 去除周期性（再次使分子保持完整）__

__\-resnr <int> \-1 从指定编号开始对残基进行重新编号__

__\-\[no\]grasp no 将原子电荷存储在B因子字段中，将原子半径存储__

__在占有率字段中__

__\-rvdw <real> 0\.12 默认的范德华半径（单位nm），用于数据库或拓扑__

__文件中不存在参数的原子__

__\-\[no\]sig56 no 使用rmin/2（范德华势最小值对应距离的一半）而__

__不是sigma/2（范德华半径的一半）__

__\-\[no\]vdwread no 从vdwradii\.dat文件中读取范德华半径，而不是__

__根据力场参数计算半径__

__\-\[no\]atom no 强制将B因子附加到每个原子__

__\-\[no\]legend no 制作B因子图例__

__\-label <string> A 为所有残基添加链标识符，以便指定其肽链归属__

__\-\[no\]conect no__

__将CONECT记录添加到输出的 \.pdb ↪ 614 文件中。只__

__有存在拓扑时才可以使用__

##### 已知问题

- __对于复杂的分子，去除周期性的子程序可能会崩溃，在这种情况下，你可以使用 gmx trjconv ↪ 343 。__

##### 补充说明

__在使用 gmx pdb2gmx创建了模拟分子体系之后，可以使用 gmx editconf为分子添加一个模拟盒子，  
也可以认为是将分子放进一个盒子中。这样，你就可以往盒子里面添加水分子，离子或者其他溶剂等等  
了。__

__\-princ这个选项可以用来对齐分子，比如使分子沿X轴对齐。例如，你想将分子中的两个残基沿Y轴  
对齐，那么就在索引文件中将这俩个残基标记一下，然后使用\-princ，根据提示就能对齐分子了。__

#### 6\.4\.30 gmx eneconv

##### 概要

__gmx eneconv \[ \-f \[<\.edr> \[\.\.\.\]\] \] \[ \-o \[<\.edr>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-offset \] \[ \-\[no\]settime \] \[ \-\[no\]sort \]  
\[ \-\[no\]rmdh \] \[ \-scalefac \] \[ \-\[no\]error \]__

##### 说明

__如果\-f选项指定了多个文件：__

__按排序后的顺序合并多个能量文件。如果同一时刻存在两帧数据，会使用后一文件中的帧。可以使用  
\-settime选项指定每个文件的起始时间。输入文件来自命令行，这样你可以使用像gmx eneconv \-f  
\*\.edr \-o fixed\.edr这样的技巧。__

__如果\-f选项指定了一个文件：__

__读入一个能量文件，应用\-dt，\-offset，\-t0和\-settime选项后将其输出到另一个能量文件，必要  
时还可以转换为不同的格式（由文件扩展名确定）。__

__程序会首先应用\-settime选项，然后应用\-dt/\-offset选项，最后应用\-b和\-e 选项来选择要输  
出的帧。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.edr> \[\.\.\.\]\] ener\.edr 能量文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.edr>\] fixed\.edr 能量文件__

__控制选项__

__选项 默认值 说明__

__\-b <real> \-1 读入第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <real> \-1 读入最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <real> 0__

__只输出时刻t除以dt的余数等于\-offset的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-offset <real> 0 \-dt选项的时间偏移量__

__\-\[no\]settime no 交互地设定每一输入文件在新输出文件中的起始时间__

__\-\[no\]sort yes 排序能量文件（不是帧）__

__\-\[no\]rmdh no 移除自由能的块数据__

__\-scalefac \(^1\) 将能量分量乘以指定的因子  
\-\[no\]error yes 文件中出现错误时终止程序__

##### 已知问题

- __当合并轨迹时，未能正确地更新sigma和E^2（统计必需的两个量）。只有实际能量是正确的。因  
此，必须使用其他方式来计算统计数据。__

##### 补充说明

__GROMACS模拟有一个非常重要的能量输出文件，即\.edr文件。gmx eneconv就是对能量输出文件进  
行处理的程序。__

__一个模拟可以分多次进行，于是得到很多\.edr文件。使用gmx eneconv的\-f选项，然后把这些能量文  
件罗列出来，就可以对这些能量文件进行合并，并输出一个完整的能量文件。如果几个能量文件中有重  
复的时间帧，那么后一个读入的能量文件将覆盖前一个。也可以使用\-settime选项对每一个输入文件的  
起始时间进行设置，以免互相覆盖。如下是一个示例：__

__eneconv \-o fixed\.edr \-f \*\.edr__

__即对当前目录下所有\.edr文件进行合并，然后输出为fixed\.edr文件。__

__当使用\-f选项读入单独一个能量文件时，可以配合其他参数对能量文件进行编辑。__

#### 6\.4\.31 gmx enemat

##### 概要

__gmx enemat \[ \-f \[<\.edr>\] \] \[ \-groups \[<\.dat>\] \] \[ \-eref \[<\.dat>\] \]  
\[ \-emat \[<\.xpm>\] \] \[ \-etot \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]sum \]  
\[ \-skip \] \[ \-\[no\]mean \] \[ \-nlevels \] \[ \-max \]  
\[ \-min \] \[ \-\[no\]coulsr \] \[ \-\[no\]coul14 \] \[ \-\[no\]ljsr \]  
\[ \-\[no\]lj14 \] \[ \-\[no\]bhamsr \] \[ \-\[no\]free \] \[ \-temp \]__

##### 说明

__gmx enemat用于从能量文件（\-f）中提取能量矩阵。使用 \-groups选项时必须指定一个文件，其中  
每行包含一个要使用的原子组。通过查找名称对应于原子组对名称的能量组，程序可以从能量文件中提  
取这些组的相互作用能的矩阵，例如，如果\-groups文件中包含：__

__2  
Protein  
SOL__

__程序会预期能量文件中包含具有Coul\-SR:Protein\-SOL 和LJ:Protein\-SOL这类名称的能量组（尽管  
同时分析许多组时gmx enemat最有用）。不同能量类型的矩阵会分开输出，由\-\[no\]coul，\-\[no\]coulr，  
\-\[no\]coul14，\-\[no\]lj，\-\[no\]lj14，\-\[no\]bham和\-\[no\]free 选项控制。最后，可以计算每组的  
总相互作用能（\-etot）。__

__可以使用以下公式计算自由能的近似值：E\_free = E\_0 \+ kT log\(<exp\(\(E\-E\_0\)/kT\)>\)，其中<>代表  
时间平均。可以提供一个包含参考自由能的文件，用以计算相对于某个参考状态的自由能差值。参考文  
件中组的名称（如残基名称）应当与\-groups文件中使用的组名称对应，但在比较时会忽略\-groups  
中追加的数字（如残基编号）。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.edr>\] ener\.edr 可选 能量文件__

__\-groups \[<\.dat>\] groups\.dat 通用数据文件__

__\-eref \[<\.dat>\] eref\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-emat \[<\.xpm>\] emat\.xpm X PixMap兼容的矩阵文件__

__\-etot \[<\.xvg>\] energy\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]sum no 对所选的能量项进行求和，而不是全部显示出来__

__\-skip \(^0\) 数据点之间跳过的帧数，即输出的帧间隔  
\-\[no\]mean yes 与\-groups同用时，抽取平均能量矩阵而不是每一时间步的  
矩阵  
\-nlevels 20 矩阵颜色的水平数  
\-max 1e\+20 最大能量值  
\-min \-1e\+20 最小能量值  
\-\[no\]coulsr yes 抽取短程库仑能  
\-\[no\]coul14 no 抽取1\-4库仑能  
\-\[no\]ljsr yes 抽取短程Lennard\-Jones能  
\-\[no\]lj14 no 抽取1\-4 Lennard\-Jones能  
\-\[no\]bhamsr no 抽取短程Buckingham能  
\-\[no\]free yes 计算自由能  
\-temp \(^300\) 自由能计算时的参考温度__

#### 6\.4\.32 gmx energy

##### 概要

__gmx energy \[ \-f \[<\.edr>\] \] \[ \-f2 \[<\.edr>\] \] \[ \-s \[<\.tpr>\] \] \[ \-o \[<\.xvg>\] \]  
\[ \-viol \[<\.xvg>\] \] \[ \-pairs \[<\.xvg>\] \] \[ \-corr \[<\.xvg>\] \]  
\[ \-vis \[<\.xvg>\] \] \[ \-evisco \[<\.xvg>\] \] \[ \-eviscoi \[<\.xvg>\] \]  
\[ \-ravg \[<\.xvg>\] \] \[ \-odh \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]fee \] \[ \-fetemp \]  
\[ \-zero \] \[ \-\[no\]sum \] \[ \-\[no\]dp \] \[ \-nbmin \]  
\[ \-nbmax \] \[ \-\[no\]mutot \] \[ \-\[no\]aver \] \[ \-nmol \]  
\[ \-\[no\]fluct\_props \] \[ \-\[no\]driftcorr \] \[ \-\[no\]fluc \]  
\[ \-\[no\]orinst \] \[ \-\[no\]ovec \] \[ \-acflen \] \[ \-\[no\]normalize \]  
\[ \-P \] \[ \-fitfn \] \[ \-beginfit \]  
\[ \-endfit \]__

##### 说明

__gmx energy用于从能量文件中提取各种能量项。程序会提示用户以交互方式选择要提取的能量项。__

__程序会使用全精度计算模拟中能量的平均值，RMSD和漂移（参见手册）。漂移是通过将数据拟合为最  
小二乘直线得到的。给出的总漂移是拟合的第一点和最后一点的差值。平均值的误差估计是根据 5 个块  
的块平均值得到的，计算平均时使用了全精度。使用\-nbmin和\-nbmax 选项可以对多个块长度进行误  
差估计。注意，在大多数情况下，能量文件包含了对所有MD步的平均值，或者进行平均的点数比能量  
文件中的帧数多得多。这使得gmx energy的统计输出比 \.xvg ↪ 623 输出文件中的更精确。如果能量文件  
中不存在精确平均值，上述统计数据只是单帧能量值的简单平均。__

__波动项给出了围绕最小二乘拟合的RMSD。__

__如果选择了正确的能量项，并且指定了命令行选项\-fluct\_props，程序可以计算一些与波动相关的性  
质。支持计算以下性质：__

__性质 所需能量项__

__等压热容量C\_p（NPT模拟） Enthalpy, Temp__

__等容热容量C\_v（NVT模拟） Etot, Temp__

__热膨胀系数（NPT模拟） Enthalpy, Vol, Temp__

__等温压缩系数 Vol, Temp__

__绝热体积模量 Vol, Temp__

__计算这些性质时，你必须使用\-nmol选项指定分子数。C\_p/C\_v的计算不包含任何量子效应修正。如  
果需要考虑，可以使用 gmx dos ↪ 222 程序。__

__可以使用 \-odh选项从ener\.edr 文件中提取并绘制自由能数据（哈密顿量差值和/或哈密顿量导数  
dhdl）。__

__使用\-fee选项可以计算系统相对于理想气体状态的自由能差值的估计值：__

__Delta A=A\(N,V,T\)\-A\_idealgas\(N,V,T\)=kT ln\(<exp\(U\_pot/kT\)>\)  
Delta G=G\(N,p,T\)\-G\_idealgas\(N,p,T\)=kT ln\(<exp\(U\_pot/kT\)>\)__

__其中k为Boltzmann常数，T由\-fetemp指定，平均对整个系综（或轨迹中的时间）进行。注意，原  
则上，只有平均是对整个（Boltzmann）系综进行并使用势能时，这种作法才是正确的。也可以对熵进__

##### 行估计：

__Delta S\(N,V,T\)=S\(N,V,T\)\-S\_idealgas\(N,V,T\)=\(<U\_pot>\-Delta A\)/T  
Delta S\(N,p,T\)=S\(N,p,T\)\-S\_idealgas\(N,p,T\)=\(<U\_pot>\+pV\-Delta G\)/T__

__如果指定了第二个能量文件（\-f2），会计算自由能差值：__

__dF=\-kT ln\(<exp\(\-\(E\_B\-E\_A\)/kT\)>\_A\) ,__

__其中E\_A和E\_B分别为第一个和第二个能量文件中的能量，平均对系综A进行。自由能差值的实时  
平均值会输出到\-ravg指定的文件中。注意，能量必须基于相同的轨迹计算。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.edr>\] ener\.edr 能量文件__

__\-f2 \[<\.edr>\] ener\.edr 可选 能量文件__

__\-s \[<\.tpr>\] topol\.tpr 可选 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] energy\.xvg xvgr/xmgr文件__

__\-viol \[<\.xvg>\] violaver\.xvg 可选 xvgr/xmgr文件__

__\-pairs \[<\.xvg>\] pairs\.xvg 可选 xvgr/xmgr文件__

__\-corr \[<\.xvg>\] enecorr\.xvg 可选 xvgr/xmgr文件__

__\-vis \[<\.xvg>\] visco\.xvg 可选 xvgr/xmgr文件__

__\-evisco \[<\.xvg>\] evisco\.xvg 可选 xvgr/xmgr文件__

__\-eviscoi__

__\[<\.xvg>\] eviscoi\.xvg 可选 xvgr/xmgr文件__

__\-ravg \[<\.xvg>\] runavgdf\.xvg 可选 xvgr/xmgr文件__

__\-odh \[<\.xvg>\] dhdl\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]fee no 进行自由能估计__

__\-fetemp \(^300\) 计算自由能时的参考温度  
\-zero \(^0\) 减去零点能  
\-\[no\]sum no 对所选的能量项进行求和，而不是全部显示出来  
\-\[no\]dp no 以高精度格式输出能量  
\-nbmin 5 用于误差估计的最小块数  
\-nbmax 5 用于误差估计的最大块数  
\-\[no\]mutot no 根据分量计算总偶极矩  
\-\[no\]aver no  
输出能量帧中的精确平均值和rmsd\(只适用计算 1 项的情  
况\)  
\-nmol 1 采样的分子数：能量会除以此数  
\-\[no\]fluct\_props no 计算基于能量波动的性质，如热容量  
\-\[no\]driftcorr no仅用于计算波动性质。计算波动性质前减去可观测量的漂__

移。

__\-\[no\]fluc no 计算能量波动的自相关而不是能量本身的自相关__

__\-\[no\]orinst no 分析瞬时取向数据__

__\-\[no\]ovec no 与\-oten同用时输出特征向量__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0__

__用于ACF的Legendre多项式的阶数（ 0 表示不使用）:__

__0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit <real> 0 对相关函数进行指数拟合的起始时间__

__\-endfit <real> \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

##### 补充说明

__gmx energy可提取\.edr文件中的能量数据并将结果输出为\.xvg文件，一般来说，命令为：__

__gmx energy \-f edr\_file \-o result\.xvg__

__如果加上\-b，\-e选项，可以从具体时间段提取结果而不是全部时间。__

__如果要编写bash脚本，可以使用命令管道，比如提取温度：__

__echo "temperature" | gmx energy \-f npt\.edr \-o temperature\.xvg__

__常用的一些gmx energy分析项目如下：__

- __Potential:体系势能__
- __Kinetic\-En:体系动能__
- __Total\-Energy:体系总能量，包括势能与动能__
- __Temperature:温度__
- __Pressure:体系平均压强__
- __Density:体系平均密度__
- __Pres\-XX: X方向压强__
- __Pres\-YY: Y方向压强__
- __Pres\-ZZ: Z方向压强__
- __\#Surf\*SurfTen:表面或界面张力  
gmx energy用于得到体系的各个能量，一般跑完MD之后，使用gmx energy处理ener\.edr只能得到  
体系的各个能量项。但如果想求体系中两个不同部分在模拟过程中的相互作用能，那就要使用一些小窍  
门。以下是实现的一种方法：__

__1\.根据原来的\.tpr文件建立一个新的\.tpr文件，在新的\.tpr文件中，使用索引文件明确定义感兴__

__趣的组。__

__2\.使用gmx mdrun的\-rerun选项指定原来的轨迹文件再跑一次模拟，这个过程很快。如果还想更快，__

__可以使用gmx trjconv把水分子去掉。这一个重复的模拟也产生轨迹文件，重要的是，还会产生一__

__个新的ener\.edr文件，这个文件中包含了\.tpr文件中定义的各个组能量及相互作用能（库库仑__

__相互作用能，范德华相互作用能等）。__

__3\.使用gmx energy把需要的能量项提取出来__

#### 6\.4\.33 gmx extract\-cluster\(2023\)

##### 概要

__gmx extract\-cluster \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \]  
\[ \-n \[<\.ndx>\] \] \[ \-clusters \[<\.ndx>\] \]  
\[ \-o \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-fgroup \]  
\[ \-xvg \] \[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \]  
\[ \-selrpos \] \[ \-select \] \[ \-vel \]  
\[ \-force \] \[ \-atoms \] \[ \-precision \]  
\[ \-starttime \] \[ \-timestep \] \[ \-box \]__

##### 说明

__gmx extract\-cluster可用于抽取轨迹帧，这些轨迹帧与运行gmx \-clndx后所得的簇相对应。该模块  
支持输出所有GROMACS支持的轨迹文件格式。__

__此外，该模块还提供了可用于修改额外信息的一些选项。__

__可以只将选择的部分原子写到每个簇的输出轨迹文件。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型: xtctrrcptgrog96__

__pdbtng__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构: tprgrog96pdb brk ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外索引组__

__\-clusters \[<\.ndx>\] cluster\.ndx__

__索引文件的名称,其中包含每个团簇所在__

__帧的索引编号,可以由gmx cluster \-clndx__

__得到\.__

__输出文件选项__

__选项 默认文件 类型 说明__

__\-o \[<\.xtc/\.trr/\.\.\.>\] trajout\.xtc__

__每个团簇输出轨迹文件名称的前缀: xtc__

__trrcptgrog96pdbtng__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时__

__间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束__

__时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧__

__时间的帧，即分析时两帧之间的时间间隔__

__（默认单位ps）__

__\-tu <enum> ps 时间值的单位: fs, ps, ns, us, ms, s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子\(若未设定,则假__

__定为前N个原子\)__

__\-xvg <enum> xmgrace 绘图格式: xmgrace, xmgr, none__

__\-\[no\]rmpbc yes 保证每一帧的分子都完整__

__\-\[no\]pbc yes 计算距离时应用周期性边界条件__

__\-sf <file> 使用文件提供选区__

__\-selrpos <enum> atom__

__选区参考位置: atom, res\_com, res\_cog,__

__mol\_com, mol\_cog, whole\_res\_com,__

__whole\_res\_cog, whole\_mol\_com,__

__whole\_mol\_cog, part\_res\_com,__

__part\_res\_cog, part\_mol\_com,__

__part\_mol\_cog, dyn\_res\_com,__

__dyn\_res\_cog, dyn\_mol\_com,__

__dyn\_mol\_cog__

__\-select__

__<selection> 将指定选区的粒子写入文件__

__\-vel <enum> preserved\-if\-present__

##### 如果可能,保存帧中粒子的速度:

__preserved\-if\-present, always, never__

__\-force <enum> preserved\-if\-present__

##### 如果可能,保存帧中粒子的力:

__preserved\-if\-present, always, never__

__\-atoms <enum> preserved\-if\-present__

##### 新的原子信息来自拓扑还是当前帧：

__preserved\-if\-present,__

__always\-from\-structure, never, always__

__\-precision <int> 3 设定值的输出精度__

__\-starttime <time> 0 更改第一帧的起始时间__

__\-timestep <time> 0 更改不同帧之间的时间间隔__

__\-box <vector> 输出帧中所用的新的对角盒子向量__

#### 6\.4\.34 gmx filter

##### 概要

__gmx filter \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-ol \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-oh \[<\.xtc/\.trr/\.\.\.>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-\[no\]w \] \[ \-nf \]  
\[ \-\[no\]all \] \[ \-\[no\]nojump \] \[ \-\[no\]fit \]__

##### 说明

__gmx filter用于对轨迹执行频率滤波。滤波器的形状为从\-A到\+A的cos\(pi t/A\) \+ 1，其中A为\-nf  
选项指定的值乘以输入轨迹中的时间步长。对于低通滤波，此滤波器可将周期为A的波动降低85%，周  
期为2A的波动降低50%，周期为3A的波动降低17%。程序可以输出低通和高通滤波后的轨迹。__

__选项\-ol指定低通滤波后轨迹的输出文件。每\-nf输入帧输出一次。滤波器长度和输出间隔的比值保  
证了可以很好的抑制高频运动的混叠，这有利于制作平滑的动画。此外，由于所有输入帧在输出中的权  
重相等，因此对那些与坐标存在线性关系的性质，其平均值会保持不变。如果需要输出所有帧，可以使  
用\-all选项。__

__选项\-oh指定高通滤波后轨迹的输出文件。高通滤波后的坐标会加到结构文件中的坐标上。当使用高  
通滤波时，请使用\-fit选项，或确保所用轨迹已经叠合到结构文件中的坐标上了。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ol \[<\.xtc/\.trr/\.\.\.>\] lowpass\.xtc 可选__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-oh \[<\.xtc/\.trr/\.\.\.>\] highpass\.xtc 可选__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__控制选项__

__选项 默认值 说明__

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0 只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧之__

__间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-nf <int> 10 设置低通滤波的滤波器长度和输出间隔__

__\-\[no\]all no 输出所有低通滤波后的帧__

__\-\[no\]nojump yes 移除越过盒子的原子跳跃__

__\-\[no\]fit no 将所有帧叠合到参考结构__

#### 6\.4\.35 gmx freevolume

##### 概要

__gmx freevolume \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \]  
\[ \-n \[<\.ndx>\] \] \[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-fgroup \]  
\[ \-xvg \] \[ \-\[no\]rmpbc \] \[ \-sf \]  
\[ \-selrpos \] \[ \-select \] \[ \-radius \]  
\[ \-seed \] \[ \-ninsert \]__

##### 说明

__gmx freevolume用于计算一个盒子中的自由体积与时间的函数关系。输出为自由体积所占总体积的比  
例。程序会尝试将一个指定半径的探针插入模拟盒子中，如果探针与任何原子之间的距离小于两个原子  
的范德华半径之和，就认为该位置已被占据，即非自由的。通过使用半径为 0 的探针，可以计算出真实  
的自由体积。通过使用更大半径的探针，如0\.14 nm，大致对应于水分子，可计算对应于指定大小假想  
粒子的自由体积。但请注意，由于将原子视为硬球，这些数字是非常近似的，通常只有相对变化才有意  
义，例如在不同温度下进行一系列的模拟。__

__可以选择指定的组并将其视为非自由体积。单位体积的插入次数对获得收敛的结果非常重要。使用大约  
1000/nm^3的插入次数可得到总的标准偏差，它是由轨迹的波动确定的，而不是由随机数引起的波动确  
定的。__

__所得结果非常依赖于范德华半径；我们建议使用Bondi\(1964\)给出的半径值。__

__一些作者喜欢使用分数自由体积（FFV），它的值为1\-1\.3\(1\-Free Volume\)。此值将输出到终端上。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构： tpr ↪^619 ， gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] freevolume\.xvg 可选 计算的自由体积__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时间（默认单位__

__ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的终止时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分__

__析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子（如果未设置，假定为前N个原__

__子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-select__

__<selection> 被视为排除体积一部分的原子__

__\-radius <real> 0__

__插入探针的半径（单位nm，使用 0 可得到真正的自由__

__体积）__

__\-seed \(^0\) 随机数生成器的种子（ 0 表示自动生成）。__

__\-ninsert \(^1000\) 对轨迹中的每一帧，每立方nm内探针尝试插入的次数__

#### 6\.4\.36 gmx gangle

##### 概要

__gmx gangle \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-oav \[<\.xvg>\] \] \[ \-oall \[<\.xvg>\] \] \[ \-oh \[<\.xvg>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-tu \]  
\[ \-fgroup \] \[ \-xvg \] \[ \-\[no\]rmpbc \]  
\[ \-\[no\]pbc \] \[ \-sf \] \[ \-selrpos \]  
\[ \-seltype \] \[ \-g1 \] \[ \-g2 \] \[ \-binw \]  
\[ \-group1 \] \[ \-group2 \]__

##### 说明

__gmx gangle用于计算向量之间不同类型的角度。它支持由两个位置定义的向量，也支持由三个位置定  
义的平面的法线。向量还可以是z轴或球面的局部法线。此外，angle和dihedral选项可方便地用于  
计算由三个/四个位置定义的键角和二面角。__

__角度类型通过\-g1和\-g2选项指定。如果\-g1为angle或dihedral，就不应该再指定\-g2。在这  
种情况下，\-group1应指定一个或多个选区，并且每个选区应包含位置的三联对或四联对，它们定义了  
要计算的角度。__

__如果\-g1为vector或plane，\-group1指定的选区应包含位置对（vector）或者三联对（plane）。  
对于向量，位置设定了向量的端点，对于平面，三个位置用于计算平面的法线。在这两种情况下，\-g2  
指定要使用的其他向量（见下文）。__

__指定\-g2 vector或\-g2 plane时，\-group2应指定另一组向量。\-group1和\-group2应该指定相  
同数目的选区。其中的某个选项也可以只有一个选区，在这种情况下，对另一个组中的每个选区都会使  
用相同的选区。类似地，对\-group1中的每个选区，\-group2中的相应选区应该指定相同数目的向量  
或单独一个向量。在后一种情况下，会计算这个单一向量与另一个选区中的每个向量之间的角度。__

__指定\-g2 sphnorm时，\-group2中的每个选区都应指定单一的位置，即球体的中心。第二个向量对应  
于从中心到由\-group1指定的位置的中点的向量。__

__指定\-g2 z时，不需要指定\-group2，程序会计算第一个向量与Z轴正半轴之间的角度。__

__指定\-g2 t0时，不需要指定\-group2，程序会根据第一帧中的向量计算角度。__

__有三个输出选项：\-oav指定一个xvg输出文件，其中包含每一帧的时间和平均角度。\-all指定所有  
单个角度的输出文件。\-oh指定角度直方图的输出文件。直方图分格的宽度可以使用 \-binw选项指定。  
对\-oav和\-oh，会计算在\-group1中每个选区的单独平均值/直方图。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选__

__输入结构： tpr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-oav \[<\.xvg>\] angaver\.xvg 可选 平均角度对时间的函数__

__\-oall \[<\.xvg>\] angles\.xvg 可选 所有角度对时间的函数__

__\-oh \[<\.xvg>\] anghist\.xvg 可选 角度的直方图__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

##### 读入轨迹第一帧的时间，即分析的起始时间（默认单位

__ps）__

__\-e <time> 0__

##### 读入轨迹最后一帧的时间，即分析的终止时间（默认单位

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分__

__析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子（如果未设置，假定为前N个原__

__子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，whole\_mol\_cog，__

__part\_res\_com，part\_res\_cog，part\_mol\_com，__

__part\_mol\_cog，dyn\_res\_com，dyn\_res\_cog，__

__dyn\_mol\_com，dyn\_mol\_cog__

__\-g1 <enum> angle 分析/第一个向量组的类型：angle，dihedral，__

__vector，plane__

__\-g2 <enum> none 第二个向量组的类型：none，vector，plane，t0，z，__

__sphnorm__

__\-binw <real> 1 \-oh输出文件中的分格宽度，单位为度__

__\-group1__

__<selection> 第一个分析/向量选区__

__\-group2__

__<selection> 第二个分析/向量选区__

#### 6\.4\.37 gmx genconf

##### 概要

__gmx genconf \[ \-f \[<\.gro/\.g96/\.\.\.>\] \] \[ \-trj \[<\.xtc/\.trr/\.\.\.>\] \]  
\[ \-o \[<\.gro/\.g96/\.\.\.>\] \] \[ \-nbox \] \[ \-dist \]  
\[ \-seed \] \[ \-\[no\]rot \] \[ \-maxrot \]  
\[ \-\[no\]renumber \]__

##### 说明

__gmx genconf可以将给定的坐标文件简单地堆叠起来，就像小孩子玩积木一样。程序会根据用户定义  
的尺寸（\-nbox）创建一个网格，格点间的额外空间由 \-dist指定。__

__如果指定了\-rot选项，程序不会检查格点上分子之间是否存在重叠。建议输入文件中的盒子边长至少  
等于坐标与范德华半径之和。__

__如果指定了可选的轨迹文件，则不生成构象，而是会从该文件中读取构象，经过适当平移后用于构建网  
格。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.gro/\.g96/\.\.\.>\] conf\.gro__

__结构文件： gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，__

__brk，ent，esp tpr ↪ 619__

__\-trj \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.gro/\.g96/\.\.\.>\] out\.gro__

__结构文件： gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，brk，__

__ent，esp__

##### 控制选项

##### 选项 默认值 说明

__\-nbox <vector> 1 1 1__

__盒子数目。将分子像堆积木一样堆积起来，一般按从小__

__到大的顺序定义x y z方向上的分子数，否则会出现分__

__子间距离较近的情况。最后分子的个数为nx\*ny\*nz__

__\-dist <vector> 0 0 0 盒子间的距离__

__\-seed <int> 0 随机数生成器的种子（ 0 表示自动生成）。__

__\-\[no\]rot no 随机旋转构象__

__\-maxrot <vector>__

##### 180 180

##### 180 随机旋转的最大值

__\-\[no\]renumber yes 重新编号残基__

##### 已知问题

##### • 程序应考虑格点的随机位移。

#### 6\.4\.38 gmx genion

##### 概要

__gmx genion \[ __\-s__ \[<\.tpr>\] \] \[ __\-n__ \[<\.ndx>\] \] \[ __\-p__ \[<\.top>\] \]  
\[ __\-o__ \[<\.gro/\.g96/\.\.\.>\] \] \[ __\-np__ \] \[ __\-pname__ \]  
\[ __\-pq__ \] \[ __\-nn__ \] \[ __\-nname__ \] \[ __\-nq__ \]  
\[ __\-rmin__ \] \[ __\-seed__ \] \[ __\-conc__ \] \[ __\-\[no\]neutral__ \]__

##### 说明

__gmx genion程序可以用单原子离子随机地取代溶剂分子。溶剂分子组应该连续，且所有溶剂分子的原  
子数应该相同。用户应将离子添加到拓扑文件中，或使用\-p选项自动修改拓扑文件。__

__在所有力场中，离子的分子类型，残基名称和原子名称都是大写字母的元素名称且不含电荷正负号。离  
子的分子名称应该使用\-pname 或\-nname指定，并且拓扑文件的 \[ molecule \]节段也要相应地更  
新，可以手工更新，或使用\-p选项自动更新。不要使用原子名称\!__

__具有多种电荷态的离子会添加多重度，但不含正负号，只用于不常见的态。__

__对于较大的离子，如硫酸根离子，我们建议使用 gmx insert\-molecules ↪ 264 插入离子。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s__

__\[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n__

__\[<\.ndx>\] index\.ndx 可选 索引文件__

__输入/输出文件选项__

__选项 默认文件 类型 说明__

__\-p__

__\[<\.top>\] topol\.top 可选 拓扑文件__

__输出文件选项__

__选项 默认文件 类型 说明__

__\-o \[<\.gro/\.g96/\.\.\.>\] out\.gro__

__结构文件： gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，brk，__

__ent，esp__

##### 控制选项

##### 选项 默认值 说明

__\-np \(^0\) 阳离子的数目  
\-pname  
NA 阳离子的名称  
\-pq \(^1\) 阳离子的电荷  
\-nn \(^0\) 阴离子的数目  
\-nname  
CL 阴离子的名称  
\-nq \-1 阴离子的电荷  
\-rmin 0\.6 离子间和非溶剂分子间的最小距离  
\-seed \(^0\) 随机数生成器的种子（ 0 表示自动生成）  
\-conc 0  
指定盐浓度（mol/L）。程序会添加足够多的离子以达到指定浓  
度。浓度是根据输入 \.tpr ↪ 619 文件中的盒子体积计算的。会覆盖  
\-np和\-nn选项。  
\-\[no\]neutral no__

__此选项会添加足够多的离子来中和系统，使总的净电荷为零。程__

__序会优先添加这些抗衡离子，然后再添加那些由\-np/\-nn或__

__\-conc指定的离子。__

##### 已知问题

##### • 如果指定了盐浓度，程序不会考虑系统中已有的离子。因此，实际上你需要指定要添加的盐的数

##### 目。

##### 补充说明

##### 在给蛋白质添加了水环境之后，一般要在水环境中添加离子，使模拟体系更接近真实体系。如果体系中

##### 的蛋白质本身已经带了静电荷，那么就更要给体系加几个带相反电荷的离子，使体系处于电中性。

##### 几个常用选项的说明：

- __\-np/\-nn/\-conc:带正/负电离子的数目。假如想要得到0\.1 mol/L的离子浓度到底要加多少离子，  
可以自己算一下，也可以直接使用\-conc指定离子浓度。在使用\-conc时，建议配合使用\-neutral，  
以便使体系最后处于电中性。__
- __\-pn/\-nn:指定正负离子的名称，比如NA\+或者CL\-。可以参看GROMACS安装路径/share/gromacs/  
top/下面的力场文件中离子使用的名称，也可以使用新的离子，但要在力场中定义，或者把新离  
子的itp文件使用\#include添加到体系拓扑文件中。__
- __\-seed:随机数种子。如果发现添加的离子离蛋白太近（比如说小于0\.1 nm），那么可以指定新的  
种子。__

__命令__

__gmx genion \-s topol\.tpr \-o system\_ion\.pdb \-p system\.top \-np 100 \-pname Na \-nn 100  
\-nname Cl__

__会添加 100 个Na\+离子和 100 个Cl离子，输出文件为system\_ion\.pdb文件。__

#### 6\.4\.39 gmx genrestr

##### 概要

__gmx genrestr \[ \-f \[<\.gro/\.g96/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-o \[<\.itp>\] \]  
\[ \-of \[<\.ndx>\] \] \[ \-fc \] \[ \-freeze \]  
\[ \-\[no\]disre \] \[ \-disre\_dist \] \[ \-disre\_frac \]  
\[ \-disre\_up2 \] \[ \-cutoff \] \[ \-\[no\]constr \]__

##### 说明

__基于\-f指定的文件的内容，gmx genrestr程序可以为拓扑生成一个\#include文件，其中包含一个  
原子列表编号，以及 x ， y 和 z 三个方向的力常数。也可以在命令行中指定单一的各向同性的力常数，而  
不是指定三个分量。__

__警告：位置限制是分子内的相互作用，因此它们必须被包含在拓扑中正确的\[ moleculetype \]节段  
内。\[ position\_restraints \]节段中的原子索引号必须处于相应分子类型的原子索引号的范围内。  
由于在拓扑中每个分子类型中的原子编号都是从 1 开始的，而在用于gmx genrestr的输入文件中也是  
从 1 开始连续编号的，因此gmx genrestr生成的文件只能用于第一个分子。你可能需要编辑得到的索  
引文件，删除第一个分子之后的原子对应的行，或构建一个合适的索引组作为gmx genrestr的输入。__

__可以使用\-of选项生成一个用于冻结原子的索引文件。在这种情况下，输入文件必须是 \.pdb ↪ 614 文件。__

__可以使用\-disre选项生成半个距离限制矩阵，而不是半个位置限制矩阵。该矩阵通常用于蛋白质中的  
Calpha原子，这样可以维持蛋白质的整体构象而不必将其绑定到特定的位置（如使用位置限制时那样）。__

##### 6\.4\. 命令说明 251

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.gro/\.g96/\.\.\.>\] conf\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp tpr ↪ 619__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.itp>\] posre\.itp 用于拓扑的包含文件__

__\-of \[<\.ndx>\] freeze\.ndx 可选 索引文件__

##### 控制选项

##### 选项 默认值 说明

__\-fc <vector> 1000 1000 1000 力常数（kJ/mol nm^2）__

__\-freeze <real> 0__

__如果指定了\-of选项或此选项，会输出一个索__

__引文件，其中包含B因子小于指定值的所有原__

__子的编号__

__\-\[no\]disre no 为索引中的所有原子生成距离限制矩阵__

__\-disre\_dist <real> 0\.1 生成距离限制时实际距离的范围__

__\-disre\_frac <real> 0__

##### 用作间隔而不是固定距离的比例。如果此处指定

##### 的距离比例小于前一选项指定的距离，则使用前

##### 一选项指定的距离。

__\-disre\_up2 <real> 1 距离限制的上限之间的距离，在此距离处力将变__

__为常数（参见手册）__

__\-cutoff <real> \-1__

__仅对处于截断范围内的原子对生成距离限制（单__

__位nm）__

__\-\[no\]constr no__

__生成约束矩阵而不是距离限制。会生成类型 2__

__的约束，并包含排除。__

#### 6\.4\.40 gmx grompp

##### 概要

__gmx grompp \[ \-f \[<\.mdp>\] \] \[ \-c \[<\.gro/\.g96/\.\.\.>\] \] \[ \-r \[<\.gro/\.g96/\.\.\.>\] \]  
\[ \-rb \[<\.gro/\.g96/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-p \[<\.top>\] \]  
\[ \-t \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-e \[<\.edr>\] \] \[ \-qmi \[<\.inp>\] \]  
\[ \-ref \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-po \[<\.mdp>\] \] \[ \-pp \[<\.top>\] \]  
\[ \-o \[<\.tpr>\] \] \[ \-imd \[<\.gro>\] \] \[ \-\[no\]v \] \[ \-time \]  
\[ \-\[no\]rmvsbds \] \[ \-maxwarn \] \[ \-\[no\]zero \] \[ \-\[no\]renum \]__

##### 说明

__gmx grompp（gromacs预处理器）读取分子的拓扑文件，检查其有效性，并将拓扑从分子描述展开成原  
子描述。拓扑文件中包含了分子类型和分子数目的信息，预处理器会根据需要复制每个分子。对分子类  
型的数目没有限制。键和键角可以转换为约束，转换时对氢原子和重原子可分开进行。然后程序读取一  
个坐标文件，如果需要可以由Maxwell分布生成速度。gmx grompp还会读取用于 gmx mdrun ↪ 276 的参  
数（如MD步数，时间步长，截断等）\.对 2019 版,还有读取其他一些参数，如NEMD参数，程序会  
校正这些参数使系统的净加速度为零。程序最终会生成一个二进制文件，它可以作为MD程序的唯一输  
入文件。__

__gmx grompp使用拓扑文件中的原子名称。坐标文件中的原子名称（\-c 选项）只用于检查它们是否与  
拓扑中的原子名称匹配，如果不匹配程序会给出警告信息。注意，原子名称与模拟无关，因为程序只会  
使用原子类型来生成相互作用参数。__

__gmx grompp使用内置的预处理器来解决包含，宏等问题。预处理器支持以下关键字：__

__\#ifdef VARIABLE  
\#ifndef VARIABLE  
\#else  
\#endif  
\#define VARIABLE  
\#undef VARIABLE  
\#include "filename"  
\#include__

__拓扑文件中这些语句的功能可以通过 \.mdp ↪ 612 文件中的下面两个选项进行调整：__

__define=\-DVARIABLE1\-DVARIABLE2  
include=\-I/home/john/doe__

__更多信息，可以参考C语言编程的教科书。指定 \-pp选项可以输出预处理后的拓扑文件，这样你就可  
以验证其内容。__

__使用位置限制时，必须使用\-r 选项提供一个包含限制坐标的文件（可以与\-c选项指定的文件相同）。  
对自由能计算，可以使用\-rb选项指定B拓扑的单独参考坐标，否则它们将与A拓扑的参考坐标相同。__

__程序可以从 \-t 选项指定的轨迹中读取起始坐标。程序会读取最后一帧的坐标和速度，除非指定了  
\-time选项。只有当缺少这一信息时才会使用由\-c选项指定的文件中的坐标。注意，如果 \.mdp ↪ 612 文  
件中指定了gen\_vel = yes，程序不会使用读入文件中的速度。可以使用\-e选项指定能量文件，用以  
读取Nose\-Hoover和/或Parrinello\-Rahman耦合变量。__

__gmx grompp可用于重新启动模拟（保持连续性），只需要使用\-t 选项提供一个检查点文件即可。但  
是，如果只是简单地改变运行步数以延长模拟，使用 gmx convert\-tpr ↪ 203 比使用 gmx grompp更方便。  
你只需要使用\-cpi选项将旧的检查点文件直接提供给 gmx mdrun ↪ 276 即可。如果想改变系综或输出频  
率等，那么建议使用\-t 为gmx grompp提供检查点文件，并使用\-f 提供一个新的 \.mdp ↪ 612 文件。实  
际上，保持系综（如果可能的话）仍然需要将检查点文件传递给 gmx mdrun ↪ 276 \-cpi。__

__默认情况下，程序会删除所有因构建虚拟位点而引入的具有恒定能量的成键相互作用。如果此恒定能量  
不为零，会导致总能量漂移。可以通过关闭\-rmvsbds选项来保持所有的成键相互作用。此外，所有因  
构建虚拟位点而引入的距离约束都是恒定的，它们都会被删除。如果系统中仍然存在任何涉及虚拟位点  
的约束，会导致致命错误。__

__要验证运行输入文件，请注意屏幕上显示的所有警告，并在必要时加以更正。此外还要查看mdout\.mdp__

____6\.4\.__ 命令说明 __253____

__文件的内容；其中包含注释行以及gmx grompp读取的输入信息。如果有疑问，可以使用\-debug选项  
启动gmx grompp，这会输出一个名为grompp\.log的文件，其中包含了更多信息（以及真正的调试信  
息）。你可以使用 gmx dump ↪ 227 程序查看运行输入文件的内容。 gmx check ↪ 192 程序可用于比较两个运行  
输入文件的内容。__

__使用\-maxwarn选项可以覆盖gmx grompp给出的警告，否则程序会停止输出。在某些情况下，警告无  
关紧要，但通常并非如此。建议用户在尝试使用此选项忽略警告之前仔细阅读并理解输出的警告消息。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.mdp>\] grompp\.mdp 含有MD参数的grompp输入文件__

__\-c \[<\.gro/\.g96/\.\.\.>\] conf\.gro 结构文件：brk，ent，esp gro ↪ tpr^610 ， g96 ↪^609 ， pdb ↪^614 ，__

__↪ 619__

__\-r \[<\.gro/\.g96/\.\.\.>\] restraint\.gro 可选 结构文件：brk，ent，esp gro ↪ tpr^610 ， g96 ↪^609 ， pdb ↪^614 ，__

__↪ 619__

__\-rb \[<\.gro/\.g96/\.\.\.>\] restraint\.gro 可选__

__结构文件： gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，__

__brk，ent，esp tpr ↪ 619__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-p \[<\.top>\] topol\.top 拓扑文件__

__\-t \[<\.trr/\.cpt/\.\.\.>\] traj\.trr 可选 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，__

__tng ↪ 617__

__\-e \[<\.edr>\] ener\.edr 可选 能量文件__

__\-qmi \[<\.inp>\] topol\-qmmm\.inp 可选 QM程序的输入文件__

##### 输入/输出文件选项

##### 选项 默认文件 类型 说明

__\-ref \[<\.trr/\.cpt/\.\.\.__

__>\] rotref\.trr 可选__

__全精度轨迹文件： trr ↪ 619 ， cpt ↪ 608 ，__

__tng ↪ 617__

__输出文件选项__

__选项 默认文件 类型 说明__

__\-po \[<\.mdp>\] mdout\.mdp 含有MD参数的grompp输入文件__

__\-pp \[<\.top>\] processed\.top 可选 拓扑文件__

__\-o \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-imd__

__\[<\.gro>\] imdgroup\.gro 可选 Gromos\-87格式的坐标文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]v no 显示更多信息__

__\-time <real> \-1 使用此时刻或此时刻之后的第一帧__

__\-\[no\]rmvsbds yes 删除涉及虚拟位点的具有恒定能量的成键相互作用__

__\-maxwarn <int> 0 输入处理过程中所允许的最大警告数目。不适用于正常情况，可__

__能导致系统不稳定__

__\-\[no\]zero no 对没有默认参数的成键相互作用，将其参数设置为零，而不是生__

__成错误__

__\-\[no\]renum yes 重新编号原子类型，以便尽量减少原子类型的数目__

#### 6\.4\.41 gmx gyrate

##### 概要

__gmx gyrate \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-acf \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-nmol \] \[ \-\[no\]q \]  
\[ \-\[no\]p \] \[ \-\[no\]moi \] \[ \-nz \] \[ \-acflen \]  
\[ \-\[no\]normalize \] \[ \-P \] \[ \-fitfn \]  
\[ \-beginfit \] \[ \-endfit \]__

##### 说明

__gmx gyrate用于计算分子的回旋半径，以及分子关于 x ， y 和 z 轴的回旋半径，并输出它们与时间的  
函数关系。蛋白质的回旋半径反映了蛋白质分子的体积和形状。同一体系的回旋半径越大，说明体系越  
膨松。计算时会明确地使用原子质量作为权重。__

__轴分量对应于垂直于每个轴的半径分量的质量加权均方根，例如：__

__Rg\(x\) = sqrt\(\(sum\_i m\_i \(R\_i\(y\)^2 \+ R\_i\(z\)^2\)\)/\(sum\_i m\_i\)\)。__

__使用\-nmol选项可以将分析组划分成大小相同的几个部分，以计算多个分子的回旋半径。__

__使用\-nz选项可以计算沿 z 轴方向 x\-y 切面内的2D回旋半径。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] gyrate\.xvg xvgr/xmgr文件__

__\-acf__

__\[<\.xvg>\] moi\-acf\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-nmol <int> 1 要分析的分子数__

__\-\[no\]q no 使用原子电荷的绝对值而不是质量作为权重因子__

__\-\[no\]p no 计算关于主轴的回旋半径。__

__\-\[no\]moi no 计算转动惯量（由主轴定义）__

__\-nz \(^0\) 计算2D回旋半径时沿z轴的切片数  
\-acflen \-1 ACF的长度，默认为帧数的一半  
\-\[no\]normalize yes 归一化ACF  
\-P 0  
用于ACF的Legendre多项式的阶数（ 0 表示不使用）:  
0 ， 1 ， 2 ， 3  
\-fitfn none  
拟合函数类型：none，exp，aexp，exp\_exp，exp5，  
exp7，exp9  
\-beginfit \(^0\) 对相关函数进行指数拟合的起始时间  
\-endfit \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

#### 6\.4\.42 gmx h2order

##### 概要

__gmx h2order \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-nm \[<\.ndx>\] \]  
\[ \-s \[<\.tpr>\] \] \[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-d \]  
\[ \-sl \]__

##### 说明

__gmx h2order用于计算水分子相对于盒子法线的取向。程序可以计算水分子的偶极矩与盒子轴线间夹角  
的余弦的平均值。计算时会将盒子划分为多个切片，并输出每一切片的平均取向。程序会将每一时间帧  
中的每个水分子都归属到某一切片内，归属时基于氧原子的位置进行。如果指定了\-nm选项，程序会计  
算水分子的偶极矩与从质心到氧原子的轴线之间的夹角，而不是偶极矩与盒子轴线之间的夹角。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

__\-nm \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] order\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧__

__之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-d <enum> Z 指定膜的法线方向，X，Y或Z: Z, Y, X__

__\-sl \(^0\) 计算序参数与盒子长度的函数关系，将盒子划分为指定数目的切片__

##### 已知问题

##### • 程序将整个水分子归属到某一切片时，是根据索引文件组中三个原子中的第一个原子，并假定顺

##### 序为O，H，H。名称并不重要，但顺序很关键。如果不能满足上述要求，则将水分子归属到切片

##### 时差别很大。

#### 6\.4\.43 gmx hbond

##### 概要

__gmx hbond \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-num \[<\.xvg>\] \] \[ \-g \[<\.log>\] \] \[ \-ac \[<\.xvg>\] \]  
\[ \-dist \[<\.xvg>\] \] \[ \-ang \[<\.xvg>\] \] \[ \-hx \[<\.xvg>\] \]  
\[ \-hbn \[<\.ndx>\] \] \[ \-hbm \[<\.xpm>\] \] \[ \-don \[<\.xvg>\] \]  
\[ \-dan \[<\.xvg>\] \] \[ \-life \[<\.xvg>\] \] \[ \-nhbdist \[<\.xvg>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-tu \]  
\[ \-xvg \] \[ \-a \] \[ \-r \] \[ \-\[no\]da \]  
\[ \-r2 \] \[ \-abin \] \[ \-rbin \] \[ \-\[no\]nitacc \]  
\[ \-\[no\]contact \] \[ \-shell \] \[ \-fitstart \]  
\[ \-fitend \] \[ \-temp \] \[ \-dump \]  
\[ \-max\_hb \] \[ \-\[no\]merge \] \[ \-nthreads \]  
\[ \-acflen \] \[ \-\[no\]normalize \] \[ \-P \]  
\[ \-fitfn \] \[ \-beginfit \] \[ \-endfit \]__

##### 说明

__gmx hbond用于计算并分析氢键。氢键是基于氢\-给体\-受体所成角度（ 0 为扩展值）的截断值，以及给  
体\-受体（或氢\-受体，如果指定了\-noda选项）之间距离的截断值共同决定的。OH和NH基团作为给  
体，O总是作为受体，N默认作为受体，但也可以使用\-nitacc选项将其更改为施体。程序会假定哑  
氢原子与前面的第一个非氢原子相连。__

__程序运行时需要指定用于分析的两个组，它们必须完全相同或彼此间无任何重叠原子。程序会分析两组  
之间的所有氢键。__

__如果指定了\-shell 选项，就需要指定一个额外的索引组，其中应该只包含一个原子。在这种情况下，  
计算时只会考虑以这个原子为中心，一定距离范围壳层内的原子之间的氢键。__

__指定\-ac选项可以计算氢键的速率常数，计算时采用Luzar和Chandler的模型（Nature 379:55, 1996;  
J\. Chem\. Phys\. 113:23, 2000）。如果指定了 \-contact选项则进行接触动力学分析，n\(t\)可以定义为t  
时刻不处于接触距离r范围内的所有氢键对（对应于\-r2选项使用默认值 0 ），或者处于距离r2范围内  
的所氢键有对（对应于使用\-r2选项指定了第二个截断值）。更多细节和定义请参考上述文献。__

__输出：__

- __\-num:氢键数目随时间的变化。__
- __\-ac:对所有的氢键，所有存在函数（ 0 或 1 ）的自相关函数的平均值。__
- __\-dist:所有氢键的距离分布。__
- __\-ang:所有氢键的角度分布。__
- __\-hx: n\-n\+i氢键数随时间的变化，其中n和n\+i代表残基编号，i的范围为0\-6。这包括了与蛋  
白质螺旋相关的n\-n\+3，n\-n\+4和n\-n\+5氢键。__
- __\-hbn:所有选中的组，选中组中的给体，氢和受体，所有组中的所有氢键原子，所有涉及插入的  
溶剂原子。输出很有限除非设置了\-nomerge\.__
- __\-hbm:所有帧中所有氢键的存在矩阵，也包含了溶剂插入氢键的信息。顺序与\-hbn索引文件中__

##### 的完全相同。

- __\-dan:每个时间帧中分析得到的给体和受体的数目。当使用\-shell 选项时特别有用。__
- __\-nhbdist:计算每个氢原子的氢键数，以便将结果与Raman光谱进行比较。__

__注意：\-ac，\-life，\-hbn和\-hbm选项需要的内存量正比于所选组中给体的总数乘以受体的总数。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-num \[<\.xvg>\] hbnum\.xvg xvgr/xmgr文件__

__\-g \[<\.log>\] hbond\.log 可选 日志文件__

__\-ac \[<\.xvg>\] hbac\.xvg 可选 xvgr/xmgr文件__

__\-dist \[<\.xvg>\] hbdist\.xvg 可选 xvgr/xmgr文件__

__\-ang \[<\.xvg>\] hbang\.xvg 可选 xvgr/xmgr文件__

__\-hx \[<\.xvg>\] hbhelix\.xvg 可选 xvgr/xmgr文件__

__\-hbn \[<\.ndx>\] hbond\.ndx 可选 索引文件__

__\-hbm \[<\.xpm>\] hbmap\.xpm 可选 X PixMap兼容的矩阵文件__

__\-don \[<\.xvg>\] donor\.xvg 可选 xvgr/xmgr文件__

__\-dan \[<\.xvg>\] danum\.xvg 可选 xvgr/xmgr文件__

__\-life \[<\.xvg>\] hblife\.xvg 可选 xvgr/xmgr文件__

__\-nhbdist__

__\[<\.xvg>\] nhbdist\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-a \(^30\) 角度截断值（氢\-给体\-受体，单位度）  
\-r 0\.35 距离截断值（X\-受体，单位nm，见下一个选项）  
\-\[no\]da yes 使用给体\-受体距离（如果为yes）或氢\-受体距离（如果为  
no）  
\-r2 0 第二截断距离。主要用于\-contact和\-ac选项  
\-abin 1 角度分布的分格宽度（单位：度）  
\-rbin 0\.005 距离分布的分格宽度（单位：nm）  
\-\[no\]nitacc yes 将氮原子作为受体  
\-\[no\]contact no 不查找氢键，只查找截断距离内的接触  
\-shell \-1 当>0时，只计算一个粒子周围指定距离壳层内的氢键  
\-fitstart 1  
拟合相关函数的起始时间（ps），以便得到氢键断裂和形成  
的前向和后向速率常数。与\-gemfit同用时，建议  
\-fitstart 0  
\-fitend 60  
拟合相关函数的终止时间（ps），以便得到氢键断裂和形成  
的前向和后向速率常数（仅与\-gemfit同用）  
\-temp 298\.15 温度（K），用于计算氢键断裂和重新形成的吉布斯自由能  
\-dump 0 将前N个氢键的ACF输出到单独的 \.xvg ↪^623 文件中，用于  
调试  
\-max\_hb 0 归一化氢键自相关函数时所用的理论最大氢键数。在程序估  
计错误的情况下可指定此选项。  
\-\[no\]merge yes 相同给体和受体之间的氢键，但不同氢原子作为单个氢键进  
行处理。主要用于ACF。  
\-nthreads 0  
对自相关进行并行循环时所用的线程数目\. nThreads <= 0  
意味着最大线程数。需要链接OpenMP。线程数目受限于  
内核数（OpenMP v\.3之前）或环境变量  
OMP\_THREAD\_LIMIT（OpenMP v\.3）  
\-acflen \-1 ACF的长度，默认为帧数的一半  
\-\[no\]normalize yes 归一化ACF  
\-P 0 用于ACF的Legendre多项式的阶数（^0 表示不使用）:  
0 ， 1 ， 2 ， 3  
\-fitfn none  
拟合函数类型：none，exp，aexp，exp\_exp，exp5，  
exp7，exp9  
\-beginfit \(^0\) 对相关函数进行指数拟合的起始时间  
\-endfit \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

#### 6\.4\.44 gmx helix

##### 概要

__gmx helix \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \]  
\[ \-cz \[<\.gro/\.g96/\.\.\.>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-r0 \] \[ \-\[no\]q \] \[ \-\[no\]F \]__

__\[ \-\[no\]db \] \[ \-\[no\]ev \] \[ \-ahxstart <int> \] \[ \-ahxend <int> \]__

##### 说明

__gmx helix用于计算螺旋的各种性质。程序会首先检查多肽，找到最长的螺旋部分，这是通过氢键和  
phi/psi角度确定的。然后会将这一段螺旋拟合为绕 z 轴的理想螺旋，并以原点居中。最后会计算螺旋的  
以下性质：__

- __螺旋半径（radius\.xvg 输出文件）。这只是所有Calpha原子的二维RMS偏差。计算方法为  
sqrt\(\(sum\_i \(x^2\(i\)\+y^2\(i\)\)\)/N\)，其中N为骨架原子数。理想螺旋的半径为0\.23 nm。__
- __扭转（twist\.xvg输出文件）。每个残基的平均螺旋角。对𝛼螺旋，此值为 100 度，3\-10螺旋对  
应的值更小， 5 螺旋对应的值更大。__
- __每个残基的上升距离（rise\.xvg输出文件）。每个残基的螺旋上升距离以Calpha原子 z 坐标之  
间的差值表示。对理想螺旋，此值为0\.15 nm。__
- __总螺旋长度（len\-ahx\.xvg输出文件）。螺旋的总长度，以nm为单位。此值只是平均上升距离  
（见上文）与螺旋残基数（见下文）的乘积。__
- __螺旋偶极矩（dip\-ahx\.xvg输出文件），计算时只考虑骨架原子。__
- __与理想螺旋的RMS偏差（rms\-ahx\.xvg输出文件），计算时只考虑Calpha原子__
- __平均Calpha\-Calpha二面角（phi\-ahx\.xvg输出文件）。__
- __平均phi和psi角（phipsi\.xvg输出文件）。__
- __根据Hirst和Brooks方法计算的222 nm处的椭圆度。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__输出文件选项__

__选项 默认文件 类型 说明__

__\-cz \[<\.gro/\.g96/\.\.\.>\] zconf\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp__

__控制选项__

__选项 默认值 说明__

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两__

__帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-r0 \(^1\) 序列中第一个残基的编号  
\-\[no\]q no 每一步都检查序列的哪个部分是螺旋  
\-\[no\]F yes 是否拟合到理想螺旋  
\-\[no\]db no 输出调试信息  
\-\[no\]ev no 输出一个新的“轨迹”文件用于ED  
\-ahxstart  
^0 螺旋的第一个残基  
\-ahxend \(^0\) 螺旋的最后一个残基__

#### 6\.4\.45 gmx helixorient

##### 概要

__gmx helixorient \[ \-s \[<\.tpr>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-oaxis \[<\.dat>\] \] \[ \-ocenter \[<\.dat>\] \] \[ \-orise \[<\.xvg>\] \]  
\[ \-oradius \[<\.xvg>\] \] \[ \-otwist \[<\.xvg>\] \]  
\[ \-obending \[<\.xvg>\] \] \[ \-otilt \[<\.xvg>\] \] \[ \-orot \[<\.xvg>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-xvg \]  
\[ \-\[no\]sidechain \] \[ \-\[no\]incremental \]__

##### 说明

__gmx helixorient用于计算𝛼螺旋内平均轴的坐标和方向，以及Calpha与（可选）一个侧链原子相对  
于轴的方向/向量。__

__作为输入，你需要指定一个索引组，其中的Calpha原子对应于𝛼螺旋，且残基连续。侧链方向需要另  
一个原子数目相同的索引组，包含每个残基中可以代表侧链的重原子。__

__注意，此程序不会进行任何结构叠合。__

__我们需要四个Calpha的坐标来定义螺旋轴的局部方向。__

__程序会根据Euler旋转计算倾斜/旋转，其中螺旋轴定义为局部 x 轴，残基/Calpha向量定义为 y 轴， z  
轴定义为它们的叉积。我们使用Y\-Z\-X次序的Euler旋转，这意味着我们\(1\)首先倾斜螺旋轴，\(2\)然  
后使其与残基向量垂直，\(3\)最后对其进行旋转。出于调试或其他目的，我们还将实际的Euler旋转角  
输出到theta\[1\-3\]\.xvg文件。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 轨迹文件： gro xtc ↪^621 ， trr ↪^619 ， cpt ↪^608 ，__

__↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-oaxis \[<\.dat>\] helixaxis\.dat 通用数据文件__

__\-ocenter \[<\.dat>\] center\.dat 通用数据文件__

__\-orise \[<\.xvg>\] rise\.xvg xvgr/xmgr文件__

__\-oradius \[<\.xvg>\] radius\.xvg xvgr/xmgr文件__

__\-otwist \[<\.xvg>\] twist\.xvg xvgr/xmgr文件__

__\-obending \[<\.xvg>\] bending\.xvg xvgr/xmgr文件__

__\-otilt \[<\.xvg>\] tilt\.xvg xvgr/xmgr文件__

__\-orot \[<\.xvg>\] rotation\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]sidechain no 计算侧链相对于螺旋轴的方向__

__\-\[no\]incremental no 计算旋转/倾斜的增量而不是总量__

#### 6\.4\.47 gmx hydorder

##### 概要

__gmx hydorder \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-s \[<\.tpr>\] \]  
\[ \-o \[<\.xpm> \[\.\.\.\]\] \] \[ \-or \[<\.out> \[\.\.\.\]\] \]  
\[ \-Spect \[<\.out> \[\.\.\.\]\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-d \] \[ \-bw \]__

__\[ \-sgang1 <real> \] \[ \-sgang2 <real> \] \[ \-tblock <int> \]__

__\[ \-nlevel <int> \]__

##### 说明

__gmx hydorder用于计算给定原子周围的四面体序参数。且可以同时计算角度和距离的序参数。更多细  
节请参考P\.\-L\. Chau and A\.J\. Hardwick, Mol\. Phys\., 93, \(1998\), 511\-518。__

__gmx hydorder计算盒子内3d网格中的序参数，如果盒子中存在两种相，用户可以通过指定参数  
\-sgang1和\-sgang2来定义不同时刻分开两相的2D界面（明智地选择这些参数很重要）。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xpm> \[\.\.\.\]\] intf\.xpm X PixMap兼容的矩阵文件__

__\-or \[<\.out> \[\.\.\.\]\] raw\.out 可选 通用输出文件__

__\-Spect \[<\.out> \[\.\.\.\]\] intfspect\.out 可选 通用输出文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两__

__帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-d <enum> z 膜的法线方向：z，x，y__

__\-bw <real> 1 盒子网格的分格宽度__

__\-sgang1 \(^1\) 相 1 （体相）中的四面体角参数  
\-sgang2 \(^1\) 相 2 （体相）中的四面体角参数  
\-tblock 1 一个时间块平均所用的帧数  
\-nlevel 100 2D XPixMaps中的高度的水平数__

#### 6\.4\.48 gmx insert\-molecules

##### 概要

__gmx insert\-molecules \[ \-f \[<\.gro/\.g96/\.\.\.>\] \] \[ \-ci \[<\.gro/\.g96/\.\.\.>\] \]  
\[ \-ip \[<\.dat>\] \] \[ \-n \[<\.ndx>\] \] \[ \-o \[<\.gro/\.g96/\.\.\.>\] \]  
\[ \-replace \] \[ \-sf \] \[ \-selrpos \]  
\[ \-box \] \[ \-nmol \] \[ \-try \] \[ \-seed \]  
\[ \-radius \] \[ \-scale \] \[ \-dr \]  
\[ \-rot \]__

##### 说明

__gmx insert\-molecules可以将\-nmol个系统的副本插入到盒子中，系统来自\-ci选项指定的输入文  
件。插入的位置可以是由\-f指定的溶质分子构型中的空位，或者是由\-box指定的空盒子。同时指定  
\-f 和\-box选项等同于指定\-f选项，但插入前会在溶质周围放置一个新盒子。程序运行时会忽略坐  
标文件中的任何速度。__

__程序也可以将分子插入到溶剂化的构型中，并用插入的原子代替溶剂原子。为此，可以使用\-replace  
选项指定一个可以替换的原子选区。程序假定此选区中的所有分子都由单个残基组成：此选区中与插入  
分子重叠的每个残基都会被移除，而不会妨碍插入。__

__默认情况下，插入位置是随机的（初始种子由\-seed 选项指定）。程序会不断迭代直至\-nmol 个分  
子插入盒子中。对某一位置，若已有的任何原子与插入分子任何原子之间的距离小于基于两个原子的  
范德华半径之和，则不会插入此分子。程序会读取数据文件（vdwradii\.dat）中的范德华半径，并根  
据\-scale选项指定的值对其进行缩放。如果无法在数据文件中找到所需的半径值，相应的原子会使用  
\-radius选项指定的（未缩放）距离。注意，这些半径在使用时是根据原子名称确定的，因此不同力场  
之间的区别很大。__

__程序在终止前总共会进行\-nmol\*\-try次插入尝试。如果需要填充一些小的孔洞，可以增加\-try选  
项的值。可以使用\-rot选项指定在插入尝试前是否对插入分子进行随机旋转。__

__或者，程序也可以只是将分子插入到position\.dat文件（\-ip选项指定）中指定的位置。此文件应包  
含 3 列\(x, y, z\)，它们给出了相对于输入分子位置（\-ci选项指定）的位移。因此，如果该文件应该包  
含绝对位置，那么在使用gmx insert\-molecules命令前必须把分子的中心置于\(0, 0, 0\) \(例如，可以  
使用 gmx editconf ↪ 231 \-center\)。程序会忽略该文件中以\#开头的注释。可以使用 \-dr选项指定插入  
尝试中允许的最大位移。\-try和\-rot选项以默认模式运行（见上文）。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.gro/\.g96/\.\.\.>\] protein\.gro 可选__

##### 已有构型，分子会插入此构型中：

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，brk，ent，__

__esp， tpr ↪ 619__

__\-ci \[<\.gro/\.g96/\.\.\.>\] insert\.gro 插入分子的构型： gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent，esp， tpr ↪ 619__

__\-ip \[<\.dat>\] positions\.dat 可选 预定义的插入尝试位置__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.gro/\.g96/\.\.\.>\] out\.gro 插入后的输出构型： gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent，esp__

__控制选项__

__选项 默认值 说明__

__\-replace <selection> 出现重叠时可移除的原子__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-box <vector> 0 0 0 盒子尺寸（单位：nm）__

__\-nmol \(^0\) 要插入的额外分子的个数  
\-try 10 尝试插入\-nmol乘以\-try次  
\-seed 0 随机数生成器的种子（ 0 表示自动生成）。  
\-radius 0\.105 默认的范德华距离（单位：nm）  
\-scale 0\.57  
用于数据文件share/gromacs/top/vdwradii\.dat中范  
德华半径的缩放因子。对水中的蛋白质，使用默认值  
0\.57得到的密度接近1000 g/l。  
\-dr 0 0 0 相对于\-ip文件中的位置，在x/y/z方向允许的位移  
\-rot xyz 随机旋转插入的分子：xyz，z，none__

##### 已知问题

##### • 对初始构型所有分子必须保持完整。

- __使用\-ci选项时，重复的近邻搜索会占用大量内存，\-allpair选项可以通过检查所有原子之间的  
距离来避免这个问题（但对大的体系计算较慢）。__

##### 补充说明

- __\-ci:为分子特定部位添加水环境，只在研究的分子部位添加水环境，这样可以减少原子数，节省  
计算时间__
- __\-seed:随机数种子，添加水分子时，各个水分子的位置是随机的，可以改变这个随机数种子使水  
分子重新分布__

#### 6\.4\.49 gmx lie

##### 概要

__gmx lie \[ \-f \[<\.edr>\] \] \[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-\[no\]w \] \[ \-xvg \] \[ \-Elj \] \[ \-Eqq \]  
\[ \-Clj \] \[ \-Cqq \] \[ \-ligand \]__

##### 说明

__gmx lie根据对非键能量的分析计算自由能估计值。计算时需要一个包含Coul\-\(A\-B\)，LJ\-SR\(A\-B\)  
等能量项的能量文件。__

__要正确使用gmx lie，需要进行两次模拟：一次是待研究的分子与受体结合情况下的模拟，一次是待研  
究分子在水中的模拟。两次模拟都需要指定energygrps 选项，这样Coul\-SR\(A\-B\)，LJ\-SR\(A\-B\)等  
能量项才会输出到 \.edr ↪ 609 文件中。来自水中分子模拟的数据可以为\-Elj和\-Eqq提供合适的值，这是必  
需的。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f__

__\[<\.edr>\] ener\.edr 能量文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] lie\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-Elj <real> 0 配体与溶剂间的Lennard\-Jones相互作用__

__\-Eqq <real> 0 配体与溶剂间的库仑相互作用__

__\-Clj <real> 0\.181 LIE方程中Lennard\-Jones能量分量的因子__

__\-Cqq <real> 0\.5 LIE方程中的能量库仑分量的因子__

__\-ligand <string> none 能量文件中配体的名称__

#### 6\.4\.50 gmx make\_edi

##### 概要

__gmx make\_edi \[ \-f \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-eig \[<\.xvg>\] \]  
\[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-tar \[<\.gro/\.g96/\.\.\.>\] \] \[ \-ori \[<\.gro/\.g96/\.\.\.>\] \]  
\[ \-o \[<\.edi>\] \] \[ \-xvg \] \[ \-mon \]  
\[ \-linfix \] \[ \-linacc \] \[ \-radfix \]  
\[ \-radacc \] \[ \-radcon \] \[ \-flood \]  
\[ \-outfrq \] \[ \-slope \] \[ \-linstep \]  
\[ \-accdir \] \[ \-radstep \] \[ \-maxedsteps \]  
\[ \-eqsteps \] \[ \-deltaF0 \] \[ \-deltaF \]  
\[ \-tau \] \[ \-Eflnull \] \[ \-T \]  
\[ \-alpha \] \[ \-\[no\]restrain \] \[ \-\[no\]hessian \]  
\[ \-\[no\]harmonic \] \[ \-constF \]__

##### 说明

__gmx make\_edi程序可以根据来自协方差矩阵（ gmx covar ↪ 206 ）或简正模式分析（ gmx nmeig ↪ 286 ）的  
特征向量，生成一个本性动力学（ED）采样的输入文件供mdrun 使用。在模拟过程中，ED采样可用  
于沿（生物）大分子的集约坐标（特征向量）对位置进行改变。特别地，通过促使系统沿这些集约坐  
标探索新的区域，ED采样可以提高MD模拟的采样效率。程序可以使用许多不同的算法（\-linfix，  
\-linacc，\-radfix，\-radacc，\-radcon）驱使系统沿特征向量运动，维持沿某（一组）特定坐标的  
位置不变（\-linfix），或仅仅监测位置在这些坐标上的投影（\-mon）。__

__\-mon:监测坐标在选定特征向量上的投影。  
\-linfix:沿选定特征向量进行固定步长的线性扩张。  
\-linacc:沿选定特征向量进行可接受的线性扩张。（接受在所需方向上的步进，拒绝其他的）。  
\-radfix:沿选定特征向量进行固定步长的径向扩张。  
\-radacc:沿选定特征向量进行可接受的径向扩张。（接受在所需方向上的步进，拒绝其他的）。注意：默  
认情况下，会使用初始MD结构作为第一次径向扩张循环的起点。如果指定了\-ori选项，可以读入一  
个定义外部起点的结构文件。__

__\-radcon:沿选定特征向量进行可接受径向收缩，收缩指向的目标结构由\-tar选项指定。__

__注意：每个特征向量只能选择一次。__

__\-outfrq:将投影等输出到 \.xvg ↪ 623 文件的频率（单位：步数）  
\-slope:可接受径向扩张的最小斜率。如果半径的自发增长率（单位：nm/步）小于指定的数值，会开  
始一个新的扩张循环。__

__\-maxedsteps:在新的循环开始前，径向扩张中每个循环的最大步数。__

__并行实现的注意事项：由于ED采样具有“全局”性（集约坐标等），至少在“蛋白质”方面，从实现的  
角度来看，ED采样并不太适合并行。由于并行ED需要一些额外的通信，因此预期运行性能会低于通  
常的MD模拟，特别是在进程数很多和/或ED组包含大量原子的情况下。__

__还要注意，如果ED组包含不止一个蛋白质，那么 \.tpr ↪ 619 文件中ED组的PBC表示必须正确。查看一  
下相对于参考结构的初始RMSD，模拟开始时就会输出这个数据；如果此数据远远高于比预期，那么某  
个ED分子可能沿盒子向量方向进行了偏移。__

__gmx mdrun程序运行时所有与ED相关的输出（由\-eo指定）对时间的函数都会输出到一个 \.xvg ↪ 623  
文件中，输出的间隔步数由\-outfrq选项指定。__

__注意，如果开始时合并了多个 \.edi ↪ 609 文件，在单个模拟中就可以（在不同的分子上）施加多个ED约  
束和洪泛势能。约束的施加顺序与它们出现在 \.edi ↪ 609 文件中的顺序相同。根据 \.edi ↪ 609 输入文件中的指  
定内容，输出文件中可能包含每个ED数据集的下列数据：__

- __分子叠合到参考结构的RMSD（只考虑计算ED约束前涉及叠合的原子）__
- __位置在选定特征向量上的投影__

__泛洪：__

__使用\-flood选项可以指定使用哪些特征向量计算洪泛势能，它会引起额外的力，将结构驱离由协方差  
矩阵描述的区域。如果指定了\-restrain 选项，势能会反转，这样就可以将结构保持在特定区域。__

__模拟的起点通常是存储在eigvec\.trr文件中的平均结构。可以使用\-ori选项将起点更改为构型空间  
中的任意位置。可以使用\-tau，\-deltaF0和\-Eflnull选项控制洪泛的行为。Efl为洪泛强度，会根  
据自适应洪泛的规则进行更新。tau为自适应洪泛的时间常数，大的tau值意味着慢的自适应（即增长  
慢）。deltaF0为经过tau ps模拟之后想要达到的洪泛强度。如果想使Efl保持不变，可以将\-tau设置  
为零。__

__\-alpha选项是一个用于控制洪泛势能宽度的经验参数。测试发现，当其值为 2 时，对蛋白质洪泛的大  
多数标准例子都能给出不错的结果。alpha基本上考虑了采样的不完整性，如果进行更进一步的采样，系  
综宽度会增加，这时可以使用alpha > 1。对限制，alpha < 1得到的限制势的宽度更小。__

__洪泛模拟的重新启动：如果要重新启动一个已经崩溃的洪泛模拟，请在输出文件中找到deltaF和Efl的  
值，然后手动将它们分别放入 \.edi ↪ 609 文件中的DELTA\_F0和EFL\_NULL下。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.trr/\.cpt/\.\.\.>\] eigenvec\.trr__

__全精度轨迹文件： trr ↪ 619 ， cpt ↪ 608 ，__

__tng ↪ 617__

__\-eig \[<\.xvg>\] eigenval\.xvg 可选 xvgr/xmgr文件__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-tar \[<\.gro/\.g96/\.\.\.>\] target\.gro 可选 结构文件： gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent，esp tpr ↪ 619__

__\-ori \[<\.gro/\.g96/\.\.\.>\] origin\.gro 可选 结构文件： gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent，esp tpr ↪ 619__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.edi>\] sam\.edi ED采样输入__

__控制选项__

__选项 默认值 说明__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-mon <string> 用于x投影的特征向量索引（如，1,2\-5,9;或1\-100:10__

__表示1 11 21 31\.\.\. 91 ）__

__\-linfix <string> 用于固定增量线性采样的特征向量索引__

__\-linacc <string> 用于可接受线性采样的特征向量索引__

__\-radfix <string> 用于固定增量径向扩张的特征向量索引__

__\-radacc <string> 用于可接受径向扩张的特征向量索引__

__\-radcon <string> 用于可接收径向收缩的特征向量索引__

__\-flood <string> 用于洪泛的特征向量索引__

__\-outfrq <int> 100 \.xvg ↪ 623 文件的输出频率（单位：步数）__

__\-slope <real> 0 可接受径向扩张的最小斜率__

__\-linstep__

__<string>__

__固定增量线性采样的步长（单位：nm/步）\(要放在引号中\!__

__如"1\.0 2\.3 5\.1 \-3\.1"\)__

__\-accdir <string> 可接受线性采样的方向，只考虑正负号\! \(要放在引号中\!如__

__"\-1 \+1 \-1\.1"\)__

__\-radstep <real> 0 固定增量径向扩张的步长（nm/步）__

__\-maxedsteps__

__<int>^0 每个循环的最大步数__

__\-eqsteps <int> 0 不受任何扰动时运行的步数__

__\-deltaF0 <real> 150 洪泛的目标失稳能量__

__\-deltaF \(^0\) 起始的deltaF值，默认为 0 ，非零值仅用于重启  
\-tau 0\.1 根据大，即洪泛强度不变deltaF0，洪泛强度自适应的耦合常数，^0 意味着无穷  
\-Eflnull 0 洪泛强度的起始值。洪泛强度会根据自适应洪泛方案进行更  
新。要使用恒定的洪泛强度，可将\-tau指定为 0 。  
\-T 300 T为温度，洪泛模拟需要此值  
\-alpha 1 使用alpha^2缩放高斯洪泛势能的宽度  
\-\[no\]restrain no 反转洪泛势能的符号，效果类似准简谐限制势  
\-\[no\]hessian no 特征向量和特征值来自Hessian矩阵  
\-\[no\]harmonic no 将特征值视为弹簧常数  
\-constF  
恒力洪泛：手动为由\-flood 选中的特征向量指定力（要放  
在引号内\!如"1\.0 2\.3 5\.1 \-3\.1"）。如果直接指定力，  
不需要其他洪泛参数。__

#### 6\.4\.51 gmx make\_ndx

##### 概要

__gmx make\_ndx \[ \-f \[<\.gro/\.g96/\.\.\.>\] \] \[ \-n \[<\.ndx> \[\.\.\.\]\] \] \[ \-o \[<\.ndx>\] \]  
\[ \-natoms \] \[ \-\[no\]twin \]__

##### 说明

##### 几乎每个GROMACS程序都需要使用索引组。所有程序都可以生成默认的索引组。只有当你需要特殊

__索引组时，才不得不使用gmx make\_ndx。一般情况下，整个系统会有一个默认索引组，蛋白质会有 9  
个默认索引组，每个残基名称都会生成一个默认索引组。__

__如果未提供索引文件，gmx make\_ndx也会生成这些默认组。借助命令中的索引编辑器，你可以选择原  
子，残基，链的名称及数目。如果提供了运行输入文件，你还可以选择原子类型。可以使用NOT，AND，  
OR等逻辑操作，也可以将组拆分为链，残基或原子。你还可以随意删除或重命名索引组。在编辑器中  
键入h可以获取更多详细信息。__

__索引编辑器和索引文件中的原子编号都是从 1 开始的。__

__可以使用\-twin选项复制所有索引组，并对其施加\-natoms选项指定的偏移，在设置计算电生理学双  
层膜时，这个选项非常有用。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.gro/\.g96/\.\.\.>\] conf\.gro 可选 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp tpr ↪ 619__

__\-n \[<\.ndx> \[\.\.\.\]\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.ndx>\] index\.ndx 索引文件__

__控制选项__

__选项 默认值 说明__

__\-natoms__

__<int>^0 设置原子数（默认从坐标或索引文件中读取）__

__\-\[no\]twin no 复制所有索引组，并进行\-natoms指定的偏移__

##### 补充说明

__GROMACS的索引文件，即index文件，扩展名为\.ndx，可使用gmx make\_ndx程序生成。__

__索引文件是GROMACS的重要文件，使用它可以在模拟过程中为所欲为。举一个简单的例子，如果  
想详细了解HIV整合酶切割DNA的反应机理，使用量子力学方法模拟反应位点的反应过程，而对其  
他部位使用一般的分子力学方法进行模拟。于是我们就面临一个对模拟体系进行分开定义的问题。在  
GROMACS中，我们可以使用索引文件来达到目的。基本思路是这样的，在索引文件中，定义一个独立  
的组，这个组包括反应位点附近的所有原子。在模拟的\.mdp文件中，对这个组定义使用量子力学模拟。  
对蛋白进行量子力学模拟时，一般使用洋葱模型。所谓洋葱模型，就是对反应位点使用高水平的方法，  
对距离反应位点一定半径范围内的，使用低水平的方法，然后其他部分使用分子力学方法。在这种情况  
下，就可以在索引文件中定义高水平方法组，把需要使用高水平方法的原子放到这个组中；再定义低水  
平方法组，指定使用低水平方法的原子。__

__再举一个例子，比如说在进行SMD（Steered Molecular Dynamics）时，要对蛋白膜上的一个原子或者  
残基施加作用力，那么可以建立一个索引文件，在该文件中定义一个组，把要施力的残基或者原子放到  
该组中。然后在相应的文件中就可以使用该组了。__

__gmx make\_ndx程序可用来选择原子组（要分析的某些特定原子或残基的ID标签）并创建索引文件。  
GROMACS已经定义了一些默认的组，对普通分析可能够用了，但如果你想进行更深入的分析，如为了  
在模拟中固定某些特定的组，或获得某些组的特殊能量信息，则需要使用gmx make\_ndx程序来指定这  
些组。__

__运行gmx make\_ndx后，可使用r选择残基，a选择原子，name对多组进行改名，还可以使用|表示或运  
算，&表示与运算。下面是几个简单的例子：__

- __r 56:选择 56 号残基__
- __r 1 36 37:选择不连续的残基__
- __r 3\-45:选择 3 至 45 号残基，使用连接符指定残基标号范围__
- __r 3\-15 | r 23\-67:选择 3 至 15 ， 23 至 67 号残基__
- __r 3\-15 & r 4:选择 3 至 15 号残基的主干链原子，在索引文件中， 4 号组为默认的主干链。__
- __r 1\-36 & a C N CA:使用包含&的命令指定只包含骨架原子的残基范围__

__新建索引组的默认名称（如r\_1\_36\_37）很繁琐，可以使用name命令进行修改。如name 15 Terminal可  
将组 15 的名称改为Terminal。修改后我们可以使用v命令查看名称是否修改成功，使用q命令保存修  
改并退出。__

__需要注意的一点就是，对gmx make\_ndx的选择，处理是由左向右依次执行的，&和|没有优先级别之分。  
如r 1\-3 | r 5\-9 & CA会先选择1\-3，5\-9号残基，再从中选择CA原子。__

__下面是使用示例：__

__启动程序后，程序列出默认的索引组__

__There are: 0 OTHER residues  
There are: 960 PROTEIN residues  
There are: 0 DNA residues  
Analysing Protein\.\.\.__

__0 System : 14571 atoms__

__1 Protein : 14571 atoms__

__2 Protein\-H : 7479 atoms__

__3 C\-alpha : 960 atoms__

__4 Backbone : 2880 atoms__

__5 MainChain : 3844 atoms__

__6 MainChain\+Cb : 4730 atoms__

__7 MainChain\+H : 4744 atoms__

__8 SideChain : 9827 atoms__

__9 SideChain\-H : 3635 atoms__

__nr : group\! 'name' nr name 'splitch' nr Enter: list groups  
'a': atom & 'del' nr 'splitres' nr 'l': list residues  
't': atom type | 'keep' nr 'splitat' nr 'h': help  
'r': residue 'res' nr 'chain' char  
"name": group 'case': case sensitive 'q': save and quit__

- __命令r 1\-355，显示  
Found 5467 atoms with res\.nr\. in range 1\-355__

__10 r\_1\-355 : 5467 atoms__

__0 System : 14571 atoms__

__1 Protein : 14571 atoms__

__2 Protein\-H : 7479 atoms__

__3 C\-alpha : 960 atoms__

__4 Backbone : 2880 atoms__

__5 MainChain : 3844 atoms__

__6 MainChain\+Cb : 4730 atoms__

__7 MainChain\+H : 4744 atoms__

__8 SideChain : 9827 atoms__

__9 SideChain\-H : 3635 atoms__

__10 r\_1\-355 : 5467 atoms__

__命令  
name 10 SUB\_H  
10 & 2  
显示  
Copied index group 10 'SUB\_H'  
Copied index group 2 'Protein\-H'  
Merged two groups with AND: 5467 7479 \-> 2783__

__11 SUB\_H\_&\_Protein\-H : 2783 atoms__

__命令__

__name 11 SUB\_H\_HEAVY，显示  
0 System : 14571 atoms  
1 Protein : 14571 atoms  
2 Protein\-H : 7479 atoms  
3 C\-alpha : 960 atoms  
4 Backbone : 2880 atoms  
5 MainChain : 3844 atoms  
6 MainChain\+Cb : 4730 atoms  
7 MainChain\+H : 4744 atoms  
8 SideChain : 9827 atoms  
9 SideChain\-H : 3635 atoms  
10 SUB\_H : 5467 atoms  
11 SUB\_H\_HEAVY : 2783 atoms  
12 SUB\_H\_BB : 1065 atoms__

__命令splitch 1，显示  
Found 4 chains  
1: 5467 atoms \(1 to 5467\)  
2: 5467 atoms \(5468 to 10934\)  
3: 1816 atoms \(10935 to 12750\)  
4: 1821 atoms \(12751 to 14571\)__

__命令del 5\-13，显示  
0 System : 14571 atoms  
1 Protein : 14571 atoms  
2 Protein\-H : 7479 atoms  
3 C\-alpha : 960 atoms  
4 Backbone : 2880 atoms  
5 SUB\_H\_BB : 1065 atoms  
6 SUB\_J\_BB : 1065 atoms  
7 SUB\_M\_BB : 375 atoms__

__8 SUB\_L\_BB : 375 atoms__

__命令r 886 905，显示  
9 r\_886\_905 : 40 atoms__

__命令splitat 9，显示  
0 System : 14571 atoms  
1 Protein : 14571 atoms  
2 Protein\-H : 7479 atoms  
3 C\-alpha : 960 atoms  
4 Backbone : 2880 atoms  
5 SUB\_H\_BB : 1065 atoms  
6 SUB\_J\_BB : 1065 atoms  
7 SUB\_M\_BB : 375 atoms  
8 SUB\_L\_BB : 375 atoms  
9 r\_886\_905 : 40 atoms  
10 r\_886\_905\_N\_13464 : 1 atoms  
11 r\_886\_905\_H\_13465 : 1 atoms  
\.\.\.  
32 r\_886\_905\_CM\_13486 : 1 atoms  
33 r\_886\_905\_HM1\_13487 : 1 atoms  
34 r\_886\_905\_HM2\_13488 : 1 atoms  
35 r\_886\_905\_HM3\_13489 : 1 atoms  
\.\.\.  
45 r\_886\_905\_CG\_13770 : 1 atoms  
46 r\_886\_905\_OD1\_13771 : 1 atoms  
47 r\_886\_905\_OD2\_13772 : 1 atoms  
48 r\_886\_905\_C\_13773 : 1 atoms  
49 r\_886\_905\_O\_13774 : 1 atoms__

__命令  
del 9\-31 del 13 \-21 del 16\-17  
显示  
0 System : 14571 atoms  
1 Protein : 14571 atoms  
2 Protein\-H : 7479 atoms  
3 C\-alpha : 960 atoms  
4 Backbone : 2880 atoms  
5 SUB\_H\_BB : 1065 atoms  
6 SUB\_J\_BB : 1065 atoms  
7 SUB\_M\_BB : 375 atoms  
8 SUB\_L\_BB : 375 atoms  
9 r\_886\_905\_CM\_13486 : 1 atoms  
10 r\_886\_905\_HM1\_13487 : 1 atoms  
11 r\_886\_905\_HM2\_13488 : 1 atoms  
12 r\_886\_905\_HM3\_13489 : 1 atoms__

__13 r\_886\_905\_CG\_13770 : 1 atoms__

__14 r\_886\_905\_OD1\_13771 : 1 atoms__

__15 r\_886\_905\_OD2\_13772 : 1 atoms__

#### 6\.4\.52 gmx mdmat

##### 概要

__gmx mdmat \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-mean \[<\.xpm>\] \] \[ \-frames \[<\.xpm>\] \] \[ \-no \[<\.xvg>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-xvg \]  
\[ \-t \] \[ \-nlevels \]__

##### 说明

__gmx mdmat用于计算残基对之间的最小距离组成的距离矩阵。可以使用\-sframes选项将这些距离矩  
阵存储下来，用以查看蛋白质三级结构随时间的变化。如果不明智地使用选项，生成的输出文件可能非  
常大。默认只输出对整个轨迹进行平均后的距离矩阵。同时，也可以输出整个轨迹中残基间不同原子的  
接触数。可以使用 gmx xpm2ps ↪ 363 处理输出文件，生成PostScript\(tm\)图。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr__

__结构\+质量（db）: tpr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-mean \[<\.xpm>\] dm\.xpm X PixMap兼容的矩阵文件__

__\-frames \[<\.xpm>\] dmf\.xpm 可选 X PixMap兼容的矩阵文件__

__\-no \[<\.xvg>\] num\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-t <real> 1\.5 截断距离__

__\-nlevels <int> 40 距离的离散水平数__

#### 6\.4\.53 gmx mdrun

##### 概要

__gmx mdrun \[ \-s \[<\.tpr>\] \] \[ \-cpi \[<\.cpt>\] \] \[ \-table \[<\.xvg>\] \]  
\[ \-tablep \[<\.xvg>\] \] \[ \-tableb \[<\.xvg> \[\.\.\.\]\] \]  
\[ \-rerun \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-ei \[<\.edi>\] \]  
\[ \-multidir \[__

__\[\.\.\.\]\] \] \[ \-awh \[<\.xvg>\] \]  
\[ \-membed \[<\.dat>\] \] \[ \-mp \[<\.top>\] \] \[ \-mn \[<\.ndx>\] \]  
\[ \-o \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-x \[<\.xtc/\.tng>\] \] \[ \-cpo \[<\.cpt>\] \]  
\[ \-c \[<\.gro/\.g96/\.\.\.>\] \] \[ \-e \[<\.edr>\] \] \[ \-g \[<\.log>\] \]  
\[ \-dhdl \[<\.xvg>\] \] \[ \-field \[<\.xvg>\] \] \[ \-tpi \[<\.xvg>\] \]  
\[ \-tpid \[<\.xvg>\] \] \[ \-eo \[<\.xvg>\] \] \[ \-px \[<\.xvg>\] \]  
\[ \-pf \[<\.xvg>\] \] \[ \-ro \[<\.xvg>\] \] \[ \-ra \[<\.log>\] \] \[ \-rs \[<\.log>\] \]  
\[ \-rt \[<\.log>\] \] \[ \-mtx \[<\.mtx>\] \] \[ \-if \[<\.xvg>\] \]  
\[ \-swap \[<\.xvg>\] \] \[ \-deffnm \] \[ \-xvg \]  
\[ \-dd \] \[ \-ddorder \] \[ \-npme \] \[ \-nt \]  
\[ \-ntmpi \] \[ \-ntomp \] \[ \-ntomp\_pme \]  
\[ \-pin \] \[ \-pinoffset \] \[ \-pinstride \]  
\[ \-gpu\_id \] \[ \-gputasks \] \[ \-\[no\]ddcheck \]  
\[ \-rdd \] \[ \-rcon \] \[ \-dlb \] \[ \-dds \]  
\[ \-nb \] \[ \-nstlist \] \[ \-\[no\]tunepme \] \[ \-pme \]  
\[ \-pmefft \] \[ \-bonded \] \[ \-update \] \[ \-\[no\]v \]  
\[ \-pforce \] \[ \-\[no\]reprod \] \[ \-cpt \] \[ \-\[no\]cpnum \]  
\[ \-\[no\]append \] \[ \-nsteps \] \[ \-maxh \]  
\[ \-replex \] \[ \-nex \] \[ \-reseed \]__

##### 说明

__gmx mdrun是GROMACS的主要计算化学引擎。显然，它用于执行分子动力学模拟，但它也可以用于  
执行随机动力学，能量最小化，测试粒子插入或（重新）能量计算。它还可以进行简正模式分析。在这  
种情况下，mdrun 可以根据单一的构象计算Hessian矩阵。对于常规的类似简正模式的计算，请确保提  
供的结构进行过适当的能量最小化。生成的矩阵可以使用 gmx nmeig ↪ 286 进行对角化。__

__mdrun程序会读取运行输入文件（\-s选项指定），并根据需要将拓扑分发到不同的进程。mdrun至少  
会产生四个输出文件。一个单独的日志文件（\-g 选项）。轨迹文件（\-o 选项），包含坐标，速度和可  
选的力。结构文件（\-c 选项），包含了最后一步的坐标和速度。能量文件（\-e选项）包含能量，温度，  
压力等，这些量大多也会输出到日志文件中。作为可选，坐标也可以输出到压缩轨迹文件中（\-x 选项）。__

__只有在进行自由能计算时，才会使用\-dhdl 选项。__

__如何高效地并行运行 mdrun是一个复杂的话题，用户指南中介绍了其中的许多方面。关于如何使用__

__mdrun的许多可用选项，你可以在那里找到实用的建议。__

__ED（本性动力学）采样和/或额外的洪泛势可以使用\-ei选项启用，后面指定一个 \.edi ↪ 609 文件。 \.edi ↪ 609  
文件可以使用make\_edi工具创建，或使用WHAT IF程序essdyn菜单中的选项来创建。mdrun会产  
生一个 \.xvg ↪ 623 输出文件，其中包含了位置，速度和力在选定特征向量上的投影。__

__如果在 \.mdp ↪ 612 文件中指定了用户自定义的势能函数，可以使用\-table选项将格式化的势函数表格传  
递给mdrun。mdrun会从当前目录或GMXLIB目录中读取该表格文件。GMXLIB 目录中有许多预格式化  
的表格文件，如具有普通库仑势的6\-8，6\-9，6\-10，6\-11，6\-12 Lennard\-Jones势能函数。如果存在配对  
相互作用，可以使用\-tablep选项读入配对相互作用函数的单独表格。__

__如果拓扑中存在表格成键函数，可以使用\-tableb选项读入其相互作用函数。对每种不同的表格相互  
作用类型，必须给出表格文件的名称。要使拓扑起作用，给出的文件名称必须与文件扩展名之前的字符  
序列匹配。这个名称序列为：下划线，后面跟着一个字母，代表键的b，代表键角的a 或代表二面角的  
d，最后是拓扑中使用的表格编号。注意，这些选项已废弃，将来可通过grompp提供。__

__如果 \.mdp ↪ 612 文件中指定了牵引，可以使用\-px和\-pf选项输出牵引质心的坐标和力。__

__\-membed选项的功能等同于以前的g\_membed，即将蛋白质嵌入膜中。使用此选项指定的数据文件中，  
包含了许多运行所需的设置。有关膜嵌入的更多详细信息，请参阅用户指南中的文档。可以分别使用  
\-mn和\-mp选项指定用于嵌入的索引文件和拓扑文件。__

__如果你怀疑模拟崩溃是由于原子受力过大导致的，可以试试\-pforce选项。使用这个选项，如果原子  
的受力超过指定值，可以将它的坐标和力输出到标准错误输出stderr。如果出现了无穷大的力，它也会  
终止运行。__

__包含系统完整状态的检查点文件会以固定的时间间隔（\-cpt 选项指定）输出到 \-cpo指定的文件中，  
除非\-cpt选项设置为\-1。前一个检查点文件会备份到state\_prev\.cpt，以确保系统的最近状态始终  
可用，这样即便在输出检查点文件时终止模拟，也仍然会存有最近时刻的检查点文件。使用\-cpnum选  
项可以保留所有的检查点文件，其输出文件名称中会附加模拟步数。通过从\-cpi选项指定的文件中读  
入完整状态，模拟可以继续进行。此选项的智能之处在于，如果没有找到检查点文件，GROMACS会假  
定这是一次常规运行，并从 \.tpr ↪ 619 文件的第一步开始执行。默认情况下，输出将追加到现有的输出文件  
中。检查点文件中包含了所有输出文件的校验码，这样当某些输出文件被修改，损坏或删除时，你永远  
不会丢失数据。\-cpi选项有三种使用场景：__

__\*不存名称匹配的文件：输出新的输出文件__

__\*所有文件都存在，且名称和校验码与检查点文件中的匹配：附加文件__

__\*其他情况下，不修改文件，并产生致命错误__

__使用\-noappend选项会打开新的输出文件，并将模拟部分编号添加到所有输出文件的名称中。注意，在  
所有情况下都不会重命名或覆盖检查点文件本身，除非它的名称与\-cpo选项指定的名称不匹配。__

__使用检查点时，输出会追加到先前的输出文件中，除非指定了\-noappend选项，或者不存在任何以前  
的输出文件（检查点文件除外）。要追加的文件的完整性是通过验证检查点文件中存储的校验码实现的。  
这可以避免追加文件时造成混淆或损坏。如果先前的输出文件只存在一部分，会导致致命错误，并且不  
会修改旧的输出文件，也不会打开新的输出文件。追加得到的结果与单独运行的结果相同。文件内容是  
二进制相同的，除非使用了不同的进程数或动态负载均衡，或者FFT库使用了计时优化。__

__使用\-maxh选项时，当运行时间超过\-maxh\*0\.99小时后，模拟会终止，并在进行下一次邻区搜索时输  
出检查点文件。当将nsteps 设置为\-1时，这一选项尤其有用。你可以在mdp中或使用相同名称的命  
令行选项来指定nsteps（尽管后者已废弃）。这种情况下模拟会无限运行下去，直至运行时间达到由  
\-maxh设置的限制（如果有的话），或收到信号。__

__至少可以通过三个IMD选项中的一个来激活交互式分子动力学（IMD）:使用 \-imdterm选项可以从  
分子查看器（如VMD）终止模拟。使用\-imdwait选项时，只要没有连接IMD客户端，mdrun就会  
暂停。可以使用\-imdpull选项打开IMD的远程操控功能。可以使用\-imdport选项来改变mdrun的  
监听端口。如果使用了IMD操控，原子索引和力会输出到\-if指定的文件中。__

__当使用MPI启动mdrun时，默认不会改变它的优先级。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-cpi \[<\.cpt>\] state\.cpt 可选 检查点文件__

__\-table \[<\.xvg>\] table\.xvg 可选 xvgr/xmgr文件__

__\-tablep \[<\.xvg>\] tablep\.xvg 可选 xvgr/xmgr文件__

__\-tableb \[<\.xvg> \[\.\.\.\]\] table\.xvg 可选 xvgr/xmgr文件__

__\-rerun \[<\.xtc/\.trr/\.\.\.>\] rerun\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-ei \[<\.edi>\] sam\.edi 可选 ED采样输入__

__\-multidir \[<dir> \[\.\.\.\]\] rundir 可选 运行目录__

__\-awh \[<\.xvg>\] awhinit\.xvg 可选 xvgr/xmgr文件__

__\-membed \[<\.dat>\] membed\.dat 可选 通用数据文件__

__\-mp \[<\.top>\] membed\.top 可选 拓扑文件__

__\-mn \[<\.ndx>\] membed\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.trr/\.cpt/\.\.\.>\] traj\.trr 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，__

__tng ↪ 617__

__\-x \[<\.xtc/\.tng>\] traj\_comp\.xtc 可选 压缩轨迹（tng格式或便携xdr格__

__式）__

__\-cpo \[<\.cpt>\] state\.cpt 可选 检查点文件__

__\-c \[<\.gro/\.g96/\.\.\.>\] confout\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent，esp__

__\-e \[<\.edr>\] ener\.edr 能量文件__

__\-g \[<\.log>\] md\.log 日志文件__

__\-dhdl \[<\.xvg>\] dhdl\.xvg 可选 xvgr/xmgr文件__

__\-field \[<\.xvg>\] field\.xvg 可选 xvgr/xmgr文件__

__\-tpi \[<\.xvg>\] tpi\.xvg 可选 xvgr/xmgr文件__

__\-tpid \[<\.xvg>\] tpidist\.xvg 可选 xvgr/xmgr文件__

__\-eo \[<\.xvg>\] edsam\.xvg 可选 xvgr/xmgr文件__

__\-px \[<\.xvg>\] pullx\.xvg 可选 xvgr/xmgr文件__

__\-pf \[<\.xvg>\] pullf\.xvg 可选 xvgr/xmgr文件__

__\-ro \[<\.xvg>\] rotation\.xvg 可选 xvgr/xmgr文件__

__\-ra \[<\.log>\] rotangles\.log 可选 日志文件__

__\-rs \[<\.log>\] rotslabs\.log 可选 日志文件__

__\-rt \[<\.log>\] rottorque\.log 可选 日志文件__

__\-mtx \[<\.mtx>\] nm\.mtx 可选 Hessian矩阵__

__\-if \[<\.xvg>\] imdforces\.xvg 可选 xvgr/xmgr文件__

__\-swap \[<\.xvg>\] swapions\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-deffnm <string> 为所有文件选项指定默认的文件名称__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-dd <vector> 0 0 0 区域分解格点， 0 表示自动优化__

__\-ddorder <enum> interleave DD进程顺序：interleave，pp\_pme，cartesian__

__\-npme <int> \-1 用于PME的单独进程数，\-1 表示使用猜测值__

__\-nt <int> 0 启动的总线程数（ 0 表示使用猜测值）__

__\-ntmpi <int> 0 启动的线程MPI的进程数（ 0 表示使用猜测值）__

__\-ntomp <int> 0 每个MPI进程启动的OpenMP线程数（^0 表示使__

__用猜测值）__

__\-ntomp\_pme <int> 0 每个MPI进程启动的OpenMP线程数（^0 表示使__

__用\-ntomp）__

__\-pin <enum> auto mdrun 是否应该尝试设置线程关联：auto，on，__

__off__

__\-pinoffset <int> 0 mdrun 将第一个线程关联到逻辑核的起始编号，用__

__于避免将不同mdrun 实例的线程关联到相同的核__

__\-pinstride <int> 0 逻辑核中线程的关联距离，使用^0 可以最大限度地__

__减少每个物理核上的线程数__

__\-gpu\_id <string> 可使用的GPU设备的唯一ID列表__

__\-gputasks <string> GPU设备的ID列表，将节点上的每个工作映射到__

__设备\.工作包括PP和PME\(如果有的话\)__

__\-\[no\]ddcheck yes 使用DD时，检查所有成键相互作用__

__\-rdd <real> 0__

##### 使用DD时，成键相互作用的最大距离（单位：

__nm）， 0 表示根据初始坐标确定__

__\-rcon <real> 0 P\-LINCS的最大距离（单位：nm）， 0 为估计值__

__\-dlb <enum> auto 动态负载均衡（使用DD时）: auto，no，yes__

__\-dds <real> 0\.8__

__处于\(0,1\)范围内的数，初始DD单元的大小会根据__

__此数的倒数进行放大，提供动态负载均衡的边界区__

__域，同时可以保持最小单元的大小。__

__\-nb <enum> auto 计算非键相互作用的设备：auto，cpu，gpu__

__\-nstlist <int> 0 使用Verlet缓冲容差时指定nstlist（^0 表示使用__

__猜测值）__

__\-\[no\]tunepme yes 优化PP/PME进程之间或GPU/CPU之间的PME__

__负载（ 2019 版只适用于Verlet截断方案）__

__\-pme <enum> auto 执行PME计算的设备：auto，cpu，gpu__

__\-pmefft <enum> auto 执行PME FFT计算的设备：auto，cpu，gpu__

__\-bonded <enum> auto 执行成键计算的设备：auto，cpu，gpu__

__\-update <enum> auto 执行更新和约束的设备: auto, cpu, gpu__

__\-\[no\]v no 显示更多信息__

__\-pforce <real> \-1 输出所有超过指定值的力（kJ/mol\-nm）__

__\-\[no\]reprod no 尽量避免影响二进制可重复性的优化__

__\-cpt \(^15\) 保存检查点文件的时间间隔（分钟）  
\-\[no\]cpnum no 保留检查点文件并对其名称进行编号  
\-\[no\]append yes__

__从检查点文件开始继续运行时，将输出追加到先前的__

__输出文件中，而不是将模拟部分的编号添加到所有文__

__件名中__

__\-nsteps <int> \-2 指定运行步数（\-1:无限，\-2:使用mdp选项。更__

__小的值无效）__

__\-maxh <real> \-1 运行时间达到指定值的99%后终止运行（单位：小__

__时）__

__\-replex <int> 0 尝试进行副本交换的间隔步数__

__\-nex <int> 0__

__每个副本交换间隔内执行随机交换的次数（建议__

__N^3）。设置为零或未指定值时会使用相邻副本交换。__

__\-reseed <int> \-1 用于副本交换的种子，\-1表示自动生成__

#### 6\.4\.54 gmx mindist

##### 概要

__gmx mindist \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-od \[<\.xvg>\] \] \[ \-on \[<\.xvg>\] \] \[ \-o \[<\.out>\] \]  
\[ \-ox \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-or \[<\.xvg>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-tu \] \[ \-\[no\]w \]  
\[ \-xvg \] \[ \-\[no\]matrix \] \[ \-\[no\]max \] \[ \-d \]  
\[ \-\[no\]group \] \[ \-\[no\]pi \] \[ \-\[no\]split \] \[ \-ng \]  
\[ \-\[no\]pbc \] \[ \-\[no\]respertime \] \[ \-\[no\]printresname \]__

##### 说明

__gmx mindist用于计算一个组与多个其他组之间的距离。程序会将（各组之间任意原子对的）最小距离  
和给定距离内的接触数输出到两个单独的文件。使用\-group选项时，如果另一组中的一个原子与第一  
组中的多个原子相接触，接触数只统计一次而不是多次。使用\-or选项时，程序会确定到第一组中每个  
残基的最小距离，并给出它与残基编号的函数。__

__使用\-pi选项时，程序会给出一个组与其周期映像的最小距离。这可用于检查蛋白质在模拟过程中是  
否可以感受到其自身的周期映像。计算时每个方向只考虑一个偏移，共计 26 个偏移。注意，使用\-s选  
项指定的文件需要包含周期性信息，或者使用\.tpr文件，或者使用带有CRYST1 字段的\.pdb 文件。  
程序也会给出组内的最大距离以及三个盒向量的长度。__

__此外， gmx distance ↪ 220 和 gmx pairdist ↪ 295 也可用于计算距离。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-od \[<\.xvg>\] mindist\.xvg xvgr/xmgr文件__

__\-on \[<\.xvg>\] numcont\.xvg 可选 xvgr/xmgr文件__

__\-o \[<\.out>\] atm\-pair\.out 可选 通用输出文件__

__\-ox \[<\.xtc/\.trr/\.\.\.>\] mindist\.xtc 可选__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-or \[<\.xvg>\] mindistres\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]matrix no 计算组与组之间的距离矩阵的一半__

__\-\[no\]max no 计算最大距离而不是最小距离__

__\-d <real> 0\.6 接触距离__

__\-\[no\]group no 计算接触数时，与第一组中多个原子的接触只统计 1 次__

__\-\[no\]pi no 计算与周期映像间的最小距离__

__\-\[no\]split no 在时间为零的位置划分图形__

__\-ng \(^1\) 要计算到中心组的距离时，其他组的数目  
\-\[no\]pbc yes 考虑周期性边界条件  
\-\[no\]respertime no 输出每个残基的距离时，输出每个时间点的距离  
\-\[no\]printresname no 输出残基名称__

#### 6\.4\.55 gmx mk\_angndx

##### 概要

__gmx mk\_angndx \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \] \[ \-type <enum> \] \[ \-\[no\]hyd \]__

__\[ \-hq <real> \]__

##### 说明

__gmx mk\_angndx用于创建一个索引文件，以便用于计算角度分布等。它需要使用一个运行输入文件  
（\.tpx）来获得键角，二面角等信息。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s__

__\[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-n__

__\[<\.ndx>\] angle\.ndx 索引文件__

__控制选项__

__选项 默认值 说明__

__\-type <enum> angle 角度类型：angle，dihedral，improper，__

__ryckaert\-bellemans__

__\-\[no\]hyd yes 包括质量< 1\.5的原子形成的角__

__\-hq <real> \-1 忽略质量< 1\.5，且原子电荷小于指定值的原子形成的角__

#### 6\.4\.56 gmx morph\(2019\)

##### 概要

__gmx morph \[ \-f1 \[<\.gro/\.g96/\.\.\.>\] \] \[ \-f2 \[<\.gro/\.g96/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-or \[<\.xvg>\] \] \[ \-\[no\]w \]  
\[ \-xvg \] \[ \-ninterm \] \[ \-first \]  
\[ \-last \] \[ \-\[no\]fit \]__

##### 说明

__gmx morph用于对构象进行线性插值以生成中间构象。当然这些构型完全不现实，但你可以试着进行验  
证。程序的输出采用通用轨迹的形式。中间构象的数目可以使用\-ninterm信息指定。可以使用\-first  
和\-last选项控制插值方式： 0 对应于输入结构 1 ，而 1 对应于输入结构 2 。如果指定的\-first <  
0 或\-last> 1，会根据输入结构x\_1到x\_2的途径进行外推。一般来说，如果总共有N个中间构象，  
那么中间构象x\(i\)的坐标为：__

__x\(i\) = x\_1 \+ \(first\+\(i/\(N\-1\)\)\(last\-first\)\)\(x\_2\-x\_1\)__

__最后，如果明确地进行了选择（\-or选项），程序可以计算相对于两个输入结构的RMSD。在这种情况  
下，可能需要读取索引文件，以选择要计算RMS的组。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f1 \[<\.gro/\.g96/\.\.\.>\] conf1\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp tpr ↪ 619__

__\-f2 \[<\.gro/\.g96/\.\.\.>\] conf2\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp tpr ↪ 619__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xtc/\.trr/\.\.\.>\] interm\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-or \[<\.xvg>\] rms\-interm\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-ninterm \(^11\) 中间构象的数目  
\-first 0 对应于第一个生成的结构（ 0 表示输入x\_1，见上文）  
\-last 1 对应于最后一个生成的结构（ 1 表示输入x\_2，见上文）  
\-\[no\]fit yes 插值前将第二个结构与第一个结构进行最小二乘叠合__

#### 6\.4\.56 gmx msd

##### 概要

__gmx msd \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-mol \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-fgroup \] \[ \-xvg \]  
\[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \] \[ \-selrpos \]  
\[ \-seltype \] \[ \-sel \] \[ \-type \]  
\[ \-lateral \] \[ \-trestart \] \[ \-maxtau \]  
\[ \-beginfit \] \[ \-endfit \]__

##### 说明

__gmx msd可以根据一组初始位置来计算原子的均方位移（MSD）。这为使用爱因斯坦关系式计算扩散系  
数的提供了一种简便方法。计算MSD时，可以使用\-trestart选项指定参考点之间的时间间隔。使用  
最小二乘方法将从\-beginfit到\-endfit之间的MSD\(t\)拟合为直线（D\*t \+ c），就可以计算扩散系  
数（注意，t为到参考点的时间，而不是模拟时间）。程序会给出扩散系数的误差估计。计算时将拟合区  
间分为两部分，分别拟合得到扩散系数，两个扩散系数的差值作为误差的估计值。__

__程序支持三个相互排斥的选项，用于计算不同类型的均方位移：\-type，\-lateral和\-ten。使用\-ten  
选项可以输出每个组的完整的MSD张量，输出顺序为：trace xx yy zz yx zx zy。__

__如果指定了\-mol选项，gmx msd会计算单个分子的MSD（计算时会将跨过盒子周期性边界的分子完  
整化）:对每个单独的分子，计算其质心的扩散系数。所选的索引组会被划分为分子。使用\-mol选项,只  
能选择一个索引组\.__

__通过对MSD进行线性回归就可以得到扩散系数。此外，当\-beginfit为\-1时，拟合从10%处开始，  
当\-endfit为\-1时，拟合到90%处结束。使用此选项也可以得到精确的误差估计，它是基于单个分子  
之间的统计获得的。注意，只要当MSD在\-beginfit到\-endfit之间完全呈线性时，得到的扩散系  
数和误差估计才是准确的。__

__可以使用 \-pdb选项输出一个 \.pdb ↪ 614 文件，其中包含了\-tpdb时刻系统的坐标，而B因子字段为分  
子扩散系数的平方根。此选项暗含了\-mol选项。__

__默认情况下，gmx msd会将所有轨迹帧与存储的每一帧以\-trestart间隔进行比较，因此存储的帧数与  
处理的帧数成正比。对于长轨迹/大轨迹，这会导致分析时间过长和内存不足错误，而且较高时间间隔  
的数据往往采样不足，在MSD图上往往表现为,较小时间间隔时曲线较平直,之后摇摆不定。可以使用  
\-maxtau选项设置帧比较的最大时间间隔，也可能提高性避免内存不足的问题。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选__

__输入结构: tpr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] msdout\.xvg 可选 MSD输出文件__

__\-mol__

__\[<\.xvg>\] diff\_mol\.xvg 可选 报告选区中每个分子的扩散系数__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时间（默认__

__单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0 只使用时刻t除以dt的余数等于第一帧时间的帧，__

__即分析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子（如果未设置，假定为前N__

__个原子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，__

__whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，__

__whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-sel <selection> 要计算从参考的MSD的选区__

__\-type <enum> unused 计算某一方向上的扩散系数：x，y，z,unused__

__\-lateral <enum> unused 计算横向扩散时，平面的法向：x，y，z,unused__

__\-trestart <real> 10 轨迹中重新起始点之间的时间间隔（单位：ps）__

__\-maxtau <real> 1\.79769e\+308 要计算MSD的帧之间的最大时间间隔\(单位ps\)__

__\-beginfit <real> \-1 拟合MSD的起始时间点（单位：ps），\-1 表示__

__10%__

__\-endfit <real> \-1 拟合MSD的结束时间点（单位：ps），\-1 表示__

__90%__

#### 6\.4\.57 gmx nmeig

##### 概要

__gmx nmeig \[ \-f \[<\.mtx>\] \] \[ \-s \[<\.tpr>\] \] \[ \-of \[<\.xvg>\] \] \[ \-ol \[<\.xvg>\] \]  
\[ \-os \[<\.xvg>\] \] \[ \-qc \[<\.xvg>\] \] \[ \-v \[<\.trr/\.cpt/\.\.\.>\] \]  
\[ \-xvg \] \[ \-\[no\]m \] \[ \-first \] \[ \-last \]  
\[ \-maxspec \] \[ \-T \] \[ \-P \] \[ \-sigma \]  
\[ \-scale \] \[ \-linear\_toler \] \[ \-\[no\]constr \]  
\[ \-width \]__

##### 说明

__gmx nmeig用于计算（Hessian）矩阵的特征向量/特征值，矩阵可以使用 gmx mdrun ↪ 276 计算。特征向  
量会输出到一个轨迹文件（\-v 选项指定）。其中的第一个结构对应的时刻t=0。特征向量作为输出文  
件中的帧，其序号作为步数，特征值作为时间戳。特征向量可使用 gmx anaeig ↪ 180 进行分析。使用 gmx  
nmens ↪ 288 可以根据特征向量生成结构的系综。如果使用质量加权，输出之前会将生成的特征向量缩放  
回普通笛卡尔坐标。这种情况下，在标准的笛卡尔范数中它们不再完全正交，而在质量加权范数中它们  
是完全正交的。__

__如果使用\-qcorr选项指定一个额外的文件，此程序也可用于计算热容和焓的量子校正。详细信息请参  
阅GROMACS手册第 1 章。计算结果包括减去给定温度下的简谐自由度。总的校正值会输出到终端屏  
幕上。推荐的校正方法为：__

__gmx nmeig \-s topol\.tpr \-f nm\.mtx \-first 7 \-last 10000 \-T 300 \-qc \[\-constr\]__

__如果模拟过程中对所有共价键都使用了键约束，那么应该使用 \-constr选项。否则，需要自己分析  
quant\_corr\.xvg文件。__

__为了更加灵活，程序在计算量子校正时还可以考虑虚拟位点。如果指定了\-constr和\-qc选项，程序__

__还会自动设置\-begin和\-end选项。__

__基于对简正模式频率的简谐分析，程序会计算热化学性质S0（标准熵），Cv（恒容热容量），零点能和  
内能，其计算方法与流行的量子化学程序基本相同。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f__

__\[<\.mtx>\] hessian\.mtx Hessian矩阵__

__\-s__

__\[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-of \[<\.xvg>\] eigenfreq\.xvg xvgr/xmgr文件__

__\-ol \[<\.xvg>\] eigenval\.xvg xvgr/xmgr文件__

__\-os \[<\.xvg>\] spectrum\.xvg 可选 xvgr/xmgr文件__

__\-qc \[<\.xvg>\] quant\_corr\.xvg 可选 xvgr/xmgr文件__

__\-v \[<\.trr/\.cpt/\.\.\.>\] eigenvec\.trr 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，__

__tng ↪ 617__

##### 控制选项

##### 选项 默认值 说明

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]m yes__

__对角化之前，将Hessian矩阵的元素除以所有涉及原子__

__的sqrt\(mass\)的乘积。“简正模式”分析应该使用这种__

__方法__

__\-first \(^1\) 输出的第一个特征向量  
\-last \(^50\) 输出的最后一个特征向量。\-1表示输出所有的。  
\-maxspec 4000 频谱中需要考虑的最高频率（1/cm）  
\-T 298\.15 当使用简正模式计算校正经典模拟结果时，计算熵，量  
子热容和焓时所用的温度  
\-P 1 计算熵时所用的压力（单位：bar）  
\-sigma 1 计算熵时使用的对称数。例如，水的对称数为^2 ，NH3  
的为 3 ，甲烷的为 12 。  
\-scale \(^1\) 计算热化学值之前，对频率进行缩放的因子  
\-linear\_toler 1e\-05 根据转动惯量的比值Ix/Iy和Ix/Iz来确定化合物是否  
为线性时所用的容差。  
\-\[no\]constr no 如果模拟中使用了约束而简正模式分析时未使用，计算  
量子校正时需要指定此选项。  
\-width 1 生成谱图时高斯峰的宽度（sigma）\(单位：1/cm\)__

#### 6\.4\.58 gmx nmens

##### 概要

__gmx nmens \[ \-v \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-e \[<\.xvg>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \]  
\[ \-n \[<\.ndx>\] \] \[ \-o \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-xvg \]  
\[ \-temp \] \[ \-seed \] \[ \-num \] \[ \-first \]  
\[ \-last \]__

##### 说明

__gmx nmens用于在子空间中平均结构的周围生成一个系综，子空间由一组简正模式（特征向量）定义。  
程序假定特征向量是质量加权的。沿每个特征向量的位置随机地取自高斯分布，其方差为kT与特征值  
的比值。__

__默认情况下，特征向量从 7 开始，因为前 6 个简正模式对应于平动和转动自由度。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-v \[<\.trr/\.cpt/\.\.\.>\] eigenvec\.trr__

__全精度轨迹文件： trr ↪ 619 ， cpt ↪ 608 ，__

__tng ↪ 617__

__\-e \[<\.xvg>\] eigenval\.xvg xvgr/xmgr文件__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xtc/\.trr/\.\.\.>\] ensemble\.xtc__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

##### 控制选项

##### 选项 默认值 说明

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-temp \(^300\) 以K为单位的温度  
\-seed \(^0\) 随机种子（ 0 表示自动生成）  
\-num 100 要产生的结构数  
\-first 7 要使用的第一个特征向量（\-1 表示选择）__

__\-last <int> \-1 要使用的最后一个特征向量（\-1 表示直到最后一个）__

#### 6\.4\.59 gmx nmr

##### 概要

__gmx nmr \[ \-f \[<\.edr>\] \] \[ \-f2 \[<\.edr>\] \] \[ \-s \[<\.tpr>\] \] \[ \-viol \[<\.xvg>\] \]  
\[ \-pairs \[<\.xvg>\] \] \[ \-ora \[<\.xvg>\] \] \[ \-ort \[<\.xvg>\] \]  
\[ \-oda \[<\.xvg>\] \] \[ \-odr \[<\.xvg>\] \] \[ \-odt \[<\.xvg>\] \]  
\[ \-oten \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-\[no\]w \]  
\[ \-xvg \] \[ \-\[no\]dp \] \[ \-skip \] \[ \-\[no\]aver \]  
\[ \-\[no\]orinst \] \[ \-\[no\]ovec \]__

##### 说明

__gmx nmr用于从能量文件中提取距离限制数据或取向限制数据。程序会以交互方式提示用户选择所需的  
项。__

__如果指定了\-viol 选项，会输出时间平均的违反，并重新计算运行时间平均和瞬时违反的总和。此外，  
可以使用\-pairs选项输出所选对之间的运行时间平均距离和瞬时距离。__

__选项\-ora，\-ort，\-oda，\-odr和\-odt用于分析取向限制数据。前两个选项输出取向限制，后三个  
选项输出取向与实验值的偏差。以a 结尾的选项输出时间平均值与限制的函数关系。以t结尾的选项  
会提示用户输入限制标签编号，并输出数据与时间的函数关系。可以使用\-odr选项输出RMS偏差与  
限制的函数关系。如果运行时使用了时间或系综平均的取向限制，可以使用\-orinst选项分析瞬时取  
向，而不是系综平均的取向，以及瞬时偏差，而不是时间和系综平均的偏差。__

__可以使用\-oten选项输出每个取向限制实验的分子序张量的特征值。使用\-ovec 选项还可以输出特征  
向量。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.edr>\] ener\.edr 能量文件__

__\-f2 \[<\.edr>\] ener\.edr 可选 能量文件__

__\-s \[<\.tpr>\] topol\.tpr 可选 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-viol \[<\.xvg>\] violaver\.xvg 可选 xvgr/xmgr文件__

__\-pairs__

__\[<\.xvg>\] pairs\.xvg 可选 xvgr/xmgr文件__

__\-ora \[<\.xvg>\] orienta\.xvg 可选 xvgr/xmgr文件__

__\-ort \[<\.xvg>\] orientt\.xvg 可选 xvgr/xmgr文件__

__\-oda \[<\.xvg>\] orideva\.xvg 可选 xvgr/xmgr文件__

__\-odr \[<\.xvg>\] oridevr\.xvg 可选 xvgr/xmgr文件__

__\-odt \[<\.xvg>\] oridevt\.xvg 可选 xvgr/xmgr文件__

__\-oten \[<\.xvg>\] oriten\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]dp no 以高精度格式输出能量__

__\-skip__

__<int>^0 数据点之间跳过的帧数，即输出的帧间隔__

__\-\[no\]aver no 输出能量帧中的精确平均值和rmsd（只适用计算 1 项的情况）__

__\-\[no\]orinst no 分析瞬时取向数据__

__\-\[no\]ovec no 与\-oten同用时输出特征向量__

#### 6\.4\.60 gmx nmtraj

##### 概要

__gmx nmtraj \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-v \[<\.trr/\.cpt/\.\.\.>\] \]  
\[ \-o \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-eignr \]  
\[ \-phases \] \[ \-temp \] \[ \-amplitude \]  
\[ \-nframes \]__

##### 说明

__gmx nmtraj可以根据特征向量生成虚拟轨迹，该轨迹对应于围绕平均结构的简谐笛卡尔振动。通常应  
该使用质量加权的特征向量，但也可以使用非加权的特征向量来生成正交运动。输出帧为一个覆盖整  
个周期的轨迹文件，并且第一帧为平均结构。如果将轨迹输出（或转换）为PDB格式，可以直接使用  
PyMol查看，并渲染成逼真的电影。运动振幅是根据特征值和预设温度计算的，并假定能量均分到所有  
模式上。为了在PyMol中可以清晰地显示出运动，可以指定不现实的高温来放大运动振幅。但是，要注  
意，对于大振幅运动，线性笛卡尔位移和质量加权二者都可以导致严重的结构变形，这只是笛卡尔简正  
模式模型的一个局限性。默认情况下，选择的特征向量从 7 开始，因为前 6 个简正模式对应于平动和转  
动自由度。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr__

__结构\+质量（db）: tpr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-v \[<\.trr/\.cpt/\.\.\.>\] eigenvec\.trr__

__全精度轨迹文件： trr ↪ 619 ， cpt ↪ 608 ，__

__tng ↪ 617__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xtc/\.trr/\.\.\.>\] nmtraj\.xtc__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ， tng ↪ 617__

##### 控制选项

##### 选项 默认值 说明

__\-eignr <string> 7 要使用的特征向量对应的字符（第一个为 1 ）__

__\-phases <string> 0\.0 相位对应的字符（默认为0\.0）__

__\-temp \(^300\) 温度（K）  
\-amplitude  
0\.25 特征值<=0的模式对应的振幅  
\-nframes \(^30\) 要生成的帧数__

#### 6\.4\.61 gmx nonbonded\-benchmark\(2023\)

##### 概要

__gmx nonbonded\-benchmark \[ \-o \[<\.csv>\] \] \[ \-size \] \[ \-nt \]  
\[ \-simd \] \[ \-coulomb \] \[ \-\[no\]table \]  
\[ \-combrule \] \[ \-\[no\]halflj \] \[ \-\[no\]energy \]  
\[ \-\[no\]all \] \[ \-cutoff \] \[ \-iter \]  
\[ \-warmup \] \[ \-\[no\]cycles \] \[ \-\[no\]time \]__

##### 说明

__gmx nonbonded\-benchmark为一个或多个所谓的Nbnxm非键对内核运行基准测试。非键对内核是MD  
模拟中计算量最大的部分，通常会占据运行时间的60%至90%。因此，对它们进行了高度优化，并提  
供了多种不同的设置来计算相同的物理相互作用。此外，对库仑相互作用有不同的物理处理方法，对没  
有LJ相互作用的原子也有不同的优化方法。对LJ相互作用也有不同的物理处理方法，但本工具只支  
持简单的截断，因为这是迄今为止最常用的处理方法。最后，虽然力的输出总是必要的，但能量输出只  
在某些步骤中需要。总共有 12 种相关的选项组合。当支持两种不同的SIMD设置时，组合数会增加一  
倍，达到 24 个。可以使用 \-all选项在一次调用中运行这些组合。每个内核的行为都会受到缓存行为  
的影响，而缓存行为是由所使用的硬件、系统大小和截断半径共同决定的。每个线程的原子数越多，就__

##### 需要越多的L1缓存来避免L1缓存未命中。截断半径主要影响数据重用：截断半径越大，数据重用越

##### 多，内核对缓存未命中的敏感度越低。

__OpenMP并行化可以利用一个计算节点内的多个硬件线程。在这些基准测试中，除了每次迭代启动和关  
闭单个OpenMP并行区域外，线程之间没有交互。此外，线程通过共享缓存中的数据和驱逐数据进行  
交互。使用的线程数由\-nt选项设置。线程亲和性非常重要，尤其是在使用SMT和共享缓存时。亲和  
性可以通过OpenMP库使用GOMP\_CPU\_AFFINITY环境变量进行设置。__

__基准工具会反复运行一个或多个内核并进行计时，迭代次数由\-iter 选项设定。初始内核调用是为了  
避免额外的初始缓存未中。时间记录以CPU高效、高精度的计数器周期为单位。请注意，这些时间往  
往与实际时钟周期不符。对于每个内核，工具都会报告周期总数、每次迭代的周期数以及每个周期（总  
共和有用）成对相互作用数。由于使用的是簇对列表而非原子对列表，因此还会计算一些超出截断距离  
的原子对的相互作用。计算这些原子对并无用处（除了额外的缓冲，但在此并不感兴趣），只是簇对设  
置的副作用。由于簇尺寸较小，SIMD 2xMM内核的有用原子对比率高于4xM内核，但总原子对吞吐  
量较低。最好在锁定CPU时钟的情况下运行此基准，或者任何基准测试，因为热节流会严重影响性能。  
如果无法做到这一点，可以使用\-warmup选项运行未计时的初始迭代，为处理器预热。__

__最相关的区域是每次迭代0\.1至 1 毫秒之间。因此，在运行时，体系大小最好能覆盖这一范围的两端。__

__\-simd和 \-table选项用于选择不同的实现来计算相同的物理量。这些选项的选择最好针对目标硬件进  
行优化。回顾以前的经验，我们发现只有在不支持FMA的 2 宽SIMD或 4 宽SIMD上，表格式Ewald  
修正才有用。由于所有现代架构都更宽并支持FMA，因此我们默认不使用表格。唯一的例外是不支持  
SIMD的内核，它们只支持表格。选项\-coulomb,\-combrule和\-halflj取决于力场和模拟体系的组  
成。对于水,只计算簇中一半原子的LJ相互作用的优化方法非常有用，因为在大多数水模型中，氢原子  
不涉及LJ相互作用。在MD引擎中，任何最多有一半原子具有LJ相互作用的簇都会自动使用这一内  
核。最后，\-energy选项会选择计算能量，而能量的计算通常只不频繁。__

##### 选项

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.csv>\] nonbonded\-benchmark\.csv 可选 以csv格式输出结果__

__控制选项__

__选项 默认值 说明__

__\-size <int> 1 体系尺寸为 3000 原子乘以此值__

__\-nt <int> 1 所用的OpenMP线程数__

__\-simd <enum> auto__

__SIMD类型, auto会运行所有支持的SIMD设置, no意味__

__着不支持SIMD: auto, no, 4xm, 2xmm__

__\-coulomb <enum> ewald 库仑相互作用的函数形式: ewald, reaction\-field__

__\-\[no\]table no 对Ewald校正使用查表而不是解析__

__\-combrule <enum> geometric LJ组合规则: geometric, lb, none__

__\-\[no\]halflj no 对一半原子使用LJ优化__

__\-\[no\]energy no 除力外还计算能量__

__\-\[no\]all no 对coulomb, halflj, combrule运行所有的 12 种选项组合__

__\-cutoff \(^1\) 成对列表和相互作用的截断距离  
\-iter \(^100\) 每个核心的迭代数  
\-warmup 0 初始预热的迭代数  
\-\[no\]cycles no 报告时使用cycles/pair而不是pairs/cycle  
\-\[no\]time no 报告时使用微秒而不是周期数__

#### 6\.4\.62 gmx order

##### 概要

__gmx order \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-nr \[<\.ndx>\] \]  
\[ \-s \[<\.tpr>\] \] \[ \-o \[<\.xvg>\] \] \[ \-od \[<\.xvg>\] \] \[ \-ob \[<\.pdb>\] \]  
\[ \-os \[<\.xvg>\] \] \[ \-Sg \[<\.xvg>\] \] \[ \-Sk \[<\.xvg>\] \]  
\[ \-Sgsl \[<\.xvg>\] \] \[ \-Sksl \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-d \] \[ \-sl \]  
\[ \-\[no\]szonly \] \[ \-\[no\]permolecule \] \[ \-\[no\]radial \]  
\[ \-\[no\]calcdist \]__

##### 说明

__gmx order用于计算碳尾端每个原子的序参数。对原子i，向量i\-1，i \+ 1以及轴会一起使用。索引文  
件中应该只包含用于计算的组，沿相关酰基链的等价碳原子组成的每个组都应该独立地定义。索引文件  
中不应该包含任何通用组（如System，Protein），以避免产生混乱（但这与四面体序参数无关，它只  
适用于水）。__

__gmx order 也可以给出序张量的所有对角线元素，还可以计算氘序参数Scd（默认）。如果指定了  
\-szonly选项，程序只会给出序张量的一个分量（由\-d选项指定），并计算每个切片的序参数。如果  
不指定\-szonly选项，程序会给出序张量的所有对角元素以及氘代序参数。__

__程序可以计算一个原子周围的四面体序参数。且可以同时计算角度和距离的序参数。更多细节请参考  
P\.\-L\. Chau and A\.J\. Hardwick, Mol\. Phys\. , __93__ , \(1998\), 511\-518。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

__\-nr \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] order\.xvg xvgr/xmgr文件__

__\-od \[<\.xvg>\] deuter\.xvg xvgr/xmgr文件__

__\-ob \[<\.pdb>\] eiwit\.pdb 可选 蛋白质数据库文件__

__\-os \[<\.xvg>\] sliced\.xvg xvgr/xmgr文件__

__\-Sg \[<\.xvg>\] sg\-ang\.xvg 可选 xvgr/xmgr文件__

__\-Sk \[<\.xvg>\] sk\-dist\.xvg 可选 xvgr/xmgr文件__

__\-Sgsl \[<\.xvg>\] sg\-ang\-slice\.xvg 可选 xvgr/xmgr文件__

__\-Sksl \[<\.xvg>\] sk\-dist\-slice\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-d <enum> z 膜的法线方向：z，x，y__

__\-sl <int> 1__

__计算序参数与盒子长度的函数关系，将盒子划分为指定数目__

__的切片__

__\-\[no\]szonly no 只给出序张量的Sz元素。（轴方向由\-d选项指定）__

__\-\[no\]permolecule no 计算分子平均的Scd序参数__

__\-\[no\]radial no 计算径向的膜法向__

__\-\[no\]calcdist no 计算到参考位置的距离__

##### 已知问题

##### • 该工具仅适用于饱和碳原子和联合原子力场。

##### • 对于其他情况，强烈建议使用不同的分析方法！

- __选项\-unsat声称可以对不饱和碳进行分析__
- __但此选项自添加就无法工作，因此被删除了。__

#### 6\.4\.63 gmx pairdist

##### 概要

__gmx pairdist \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-tu \] \[ \-fgroup \] \[ \-xvg \]  
\[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \] \[ \-selrpos \]  
\[ \-seltype \] \[ \-cutoff \] \[ \-type \]  
\[ \-refgrouping \] \[ \-selgrouping \]  
\[ \-ref \] \[ \-sel \]__

##### 说明

__gmx pairdist用于计算一个参考选区（由\-ref指定）与一个或多个其他选区（由\-sel指定）之间  
的成对距离。它可用于计算最小距离（默认）或最大距离（\-type max 选项）。与\-sel指定的每个选  
区的距离都是单独计算的。__

__默认情况下，会计算全局最小/最大距离。要计算更多距离（例如，与\-ref 中每个残基的最小距离），  
可以使用\-refgrouping和/或\-selgrouping来指定应该如何对每个选区中的位置进行分组。__

__计算得到的距离会输出到\-o 选项指定的文件中。如果\-ref中有N个组，而\-sel中的第一个选区有  
M个组，那么对第一个选区会输出N\*M列数据。列中包含的距离类似：r1\-s1，r2\-s1，\.\.\.，r1\-s2，r2\-s2，  
\.\.\.，其中rn为\-ref中的第n个组，sn为其他选区中的第n个组。第二个选区的距离作为单独的列排  
在第一个选区之后，依此类推。如果某些选区是动态的，那么在计算中只会使用被选中位置，但始终会  
输出相同数目的列。如果某些配对组不存在位置贡献，则会输出截断值（见下文）。__

__可以使用 \-cutoff选项指定计算距离的截断值。如果结果中包含超过截断值的距离，会将截断值输出  
到文件中。默认情况下，不会使用截断，但如果你对超过截断的值不感兴趣，或者你知道最小距离小于  
截断值，那么你应该指定此选项，这样程序可以使用基于格点的搜索，运行速度要快得多。__

__如果要计算固定位置对之间的距离， gmx distance ↪ 220 可能更合适。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构： pdb tpr ↪^619 ， gro ↪^610 ， g96 ↪^609 ，__

__↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] dist\.xvg 距离对时间的函数__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时间（默认单位__

__ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的终止时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分__

__析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子（如果未设置，假定为前N个原__

__子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，whole\_mol\_cog，__

__part\_res\_com，part\_res\_cog，part\_mol\_com，__

__part\_mol\_cog，dyn\_res\_com，dyn\_res\_cog，__

__dyn\_mol\_com，dyn\_mol\_cog__

__\-cutoff <real> 0 要考虑的最大距离__

__\-type <enum> min 要计算的距离类型：min，max__

__\-refgrouping__

__<enum> all__

__计算最小/最大距离时，将\-ref位置进行分组的方式：__

__all，res，mol，none__

__\-selgrouping__

__<enum> all__

__计算最小/最大距离时，将\-sel位置进行分组的方式：__

__all，res，mol，none__

__\-ref <selection> 用于计算距离的参考位置__

__\-sel <selection> 用于计算距离的位置__

#### 6\.4\.64 gmx pdb2gmx

##### 概要

__gmx pdb2gmx \[ \-f \[<\.gro/\.g96/\.\.\.>\] \] \[ \-o \[<\.gro/\.g96/\.\.\.>\] \] \[ \-p \[<\.top>\] \]  
\[ \-i \[<\.itp>\] \] \[ \-n \[<\.ndx>\] \] \[ \-q \[<\.gro/\.g96/\.\.\.>\] \]__

__\[ \-chainsep <enum> \] \[ \-merge <enum> \] \[ \-ff <string> \]__

__\[ \-water <enum> \] \[ \-\[no\]inter \] \[ \-\[no\]ss \] \[ \-\[no\]ter \]__

__\[ \-\[no\]lys \] \[ \-\[no\]arg \] \[ \-\[no\]asp \] \[ \-\[no\]glu \] \[ \-\[no\]gln \]__

__\[ \-\[no\]his \] \[ \-angle <real> \] \[ \-dist <real> \] \[ \-\[no\]una \]__

__\[ \-\[no\]ignh \] \[ \-\[no\]missing \] \[ \-\[no\]v \] \[ \-posrefc <real> \]__

__\[ \-vsite <enum> \] \[ \-\[no\]heavyh \] \[ \-\[no\]deuterate \]__

__\[ \-\[no\]chargegrp \] \[ \-\[no\]cmap \] \[ \-\[no\]renum \] \[ \-\[no\]rtpres \]__

##### 说明

__gmx pdb2gmx读入一个 \.pdb ↪ 614 （或 \.gro ↪ 610 ）文件和一些数据库文件，为分子添加氢原子，并生成坐标  
文件和GROMACS格式的拓扑文件。坐标文件可以选择GROMACS\(GROMOS\)格式或 \.pdb ↪ 614 格式。  
对这些文件进行后处理就可以生成运行输入文件。__

__gmx pdb2gmx查找力场时，会在当前工作目录和GROMACS库目录下的\.ff 子目录  
中搜寻 forcefield\.itp文件，库目录是根据可执行文件的路径推断出来的，也可以由GMXLIB 环境  
变量指定。默认情况下，当找到可用的力场文件后，程序会提示你选择其中的一个力场，但也可以在  
命令行中使用\-ff选项指定其中一个力场的短名称。在这种情况下，gmx pdb2gmx只会搜寻相应的  
\.ff目录。__

__选择了一种力场后，程序只会读取相应力场目录下的所有文件。如果要修改或添加一个残基类型，可以  
将力场目录从GROMACS库目录复制到当前工作目录。如果想添加一个新的蛋白质残基类型，则需要  
修改库目录中的residuetypes\.dat文件，或将整个库目录复制到本地目录，并将环境变量GMXLIB设  
置为新的目录。有关文件格式的详细信息，请查阅参考手册第 5 章↪ 524 。__

__注意， \.pdb ↪ 614 文件只是一种文件格式，不一定非要包含蛋白质结构。只要GROMACS的数据库支持，  
任何类型的分子都可以使用gmx pdb2gmx进行转换。如果数据库不支持，你可以自己添加。__

__这个程序的智能程度有限，它需要读取一系列的数据库文件，这样才能添加残基之间的特殊化学键（如  
Cys\-Cys，Heme\-His等），如果有必要，也可以手动添加这些特殊的成键。程序可以提示用户选择LYS，  
ASP，GLU，CYS或HIS残基的质子化状态。对于Lys残基，可以选择中性状态（即NZ上有两个质  
子）或质子化状态（三个质子，默认）;对于Asp和Glu残基，可以选择非质子化状态（默认）或质子  
化状态；对于His残基，质子可以位于ND1，或NE2，或两者之上。默认情况下，这些选择是自动完成  
的。对于His残基，程序是基于最佳氢键构象进行选择的。氢键是根据简单的几何标准判定的，该标准  
由氢\-给体\-受体所成角度的最大值以及给体\-受体的最大距离指定，而最大角度和最大距离可以分别使用  
\-angle和\-dist选项设定。__

__如果指定了\-ter选项，可以交互地选择蛋白质N端和C端的质子化状态。默认情况下蛋白质的两个  
末端是离子化的（即NH3\+和COO\-）。对只含一种残基的蛋白质链，有些力场支持将其设置为两性离  
子形式，但对于多肽链，不应该指定这些选项。AMBER力场中蛋白质两端的残基具有独特的形式，与  
\-ter选项的机制不相容。如果要使用AMBER力场的形式，需要在N端或C端残基对应的名称前分别  
加上N或C，并保证坐标文件的格式相同。或者，也可以使用特殊命名的末端残基（如ACE，NME）。__

__处理PDB文件时，将不同的链分开并不是非常简单的事，因为在用户生成的PDB文件中链的组织方式  
不同，使用的标记也经常变化，有时需要合并PDB文件中使用TER标记分开的两个部分，例如，想要  
使用二硫键或距离限制将两条蛋白质链连接起来，或者蛋白质上结合了HEME基团的情况下。在这种  
情况下，多条链应该包含在同一个\[ moleculetype \]定义中。为了解决这个问题，gmx pdb2gmx可  
以使用两个单独的选项。首先，可以使用\-chainsep选项选择何时开始一个新的化学链，并在适用时  
为链添加末端。这可以根据PDB文件中存在的TER记录，链标识符的改变，或者这两个条件中的一个  
或两个进行。还可以完全交互地进行选择。此外，还可以使用\-merge选项控制在添加（或不添加）所__

##### 有化学末端后，如何将多条链合并为一个分子类型。这个选项可以指定关闭（即不进行合并），或将所有

##### 非水分子的链都合并到一个分子类型中，或交互地进行选择。

__gmx pdb2gmx还会检查 \.pdb ↪ 614 文件中的原子占据率字段。如果任何一个原子的占据率不是 1 ，说明这  
个原子在结构中的位置没有确定得很好，程序会给出警告消息。如果一个 \.pdb ↪ 614 文件不是来自X射线  
晶体衍射确定的结构，可能所有的占据率字段都是零。无论如何，在使用gmx pdb2gmx时用户必须首  
先验证输入PDB文件的正确性（阅读PDB文件作者的原始文章\!）。__

__在处理过程中，PDB文件中原子将根据GROMACS的约定进行重新排序。如果指定了\-n 选项，程序  
会生成一个索引文件，其中包含了以相同方式重新排序的组。这样你就可以将GROMOS轨迹和坐标文  
件转换为GROMOS。需要注意的是，这种作法有一个限制：因为重新排序是在去除输入文件中的氢原  
子之后，在添加新的氢原子之前进行的。这意味着你不能使用\-ignh选项。__

__\.gro ↪ 610 和\.g96文件格式不支持链标识符。因此，如果需要转换一个包含多条链的 \.pdb ↪ 614 文件，最好  
使用\-o选项将结果输出为 \.pdb ↪ 614 文件。__

__使用\-vsite选项可以移除氢原子和快速的反常二面角运动。通过将氢原子转换为虚拟位点并固定键角，  
即固定它们相对于相邻原子的位置，可以移除键角运动以及面外运动。此外，标准氨基酸芳环中的所有  
原子（即PHE，TRP，TYR和HIS）都可以转换为虚拟位点，从而移除这些环中快速的反常二面角波  
动（但此功能已经废弃）。注意，在这种情况下，所有其他氢原子都会被转换为虚拟位点。所有被转换为  
虚拟位点的原子的质量会添加到重原子上。__

__另外，也可以指定 \-heavyh选项，这样氢原子的质量会增加为原来的 4 倍，从而可以减慢二面角的运  
动。这种方法也适用于水中的氢原子，用于减慢水分子的转动。在这种情况下，应当从成键（重）原子  
的质量中减去氢原子增加的质量，以维持系统的总质量不变。__

__作为一种特殊情况，根据还会考虑闭环（或环状）分子。gmx pdb2gmx可以通过评估给定链的末端原  
子之间的距离自动判断是否存在环状分子。如果距离大于 \-sb（“短键警告距离Short bond warning  
distance”，默认值为0\.05 nm），并且小于\-lb（“长键警告距离Long bond warning distance”，默认值  
为0\.25 nm）,分子会被视为闭环分子，并进行相应处理。请注意，这并不会检测周期性边界上的环状键。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.gro/\.g96/\.\.\.>\] protein\.pdb 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，__

__brk，ent，esp tpr ↪ 619__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.gro/\.g96/\.\.\.>\] conf\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp__

__\-p \[<\.top>\] topol\.top 拓扑文件__

__\-i \[<\.itp>\] posre\.itp 用于拓扑的包含文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-q \[<\.gro/\.g96/\.\.\.>\] clean\.pdb 可选 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp__

##### 控制选项

##### 选项 默认值 说明

__\-chainsep <enum> id\_or\_ter__

__使用哪种条件判断PDB文件中一条新链的开始（并添__

__加末端）:id\_or\_ter，id\_and\_ter，ter，id，__

__interactive__

__\-merge <enum> no 是否将多条链合并为单个\[ moleculetype \]: no，__

__all，interactive__

__\-ff <string> select 指定力场，默认交互式选择。使用\-h 查看信息。__

__\-water <enum> select__

__指定要使用的水模型：select，none，spc，spce，__

__tip3p，tip4p，tip5p，tips3p。指定此参数会在拓__

__扑文件中添加水分子的拓扑信息__

__\-\[no\]inter no 指定此选项，接下来的 8 个选项需要交互式地进行选择__

__\-\[no\]ss no 交互式地选择二硫键__

__\-\[no\]ter no 交互式地选择末端，默认为带电荷末端（默认）__

__\-\[no\]lys no 交互式地选择LYS赖氨酸残基类型，默认为带电荷状__

__态__

__\-\[no\]arg no 交互式地选择ARG精氨酸残基类型，默认为带电荷状__

__态__

__\-\[no\]asp no 交互式地选择ASP天冬氨酸残基类型，默认为带电荷__

__状态__

__\-\[no\]glu no 交互式地选择GLU谷氨酸残基类型，默认为带电荷状__

__态__

__\-\[no\]gln no 交互式地选择GLN谷氨酰胺残基类型，默认为带电荷__

__状态__

__\-\[no\]his no 交互式地选择断 HIS组氨酸残基类型，默认根据氢键判__

__\-angle <real> 135 氢键判断标准中氢\-给体\-受体角度的最小值（单位：度）__

__\-dist <real> 0\.3 氢键判断标准中给体\-受体距离的最大值（单位：nm）__

__\-\[no\]una no__

__将phenylalanine苯丙氨酸，tryptophane色氨酸和__

__tyrosine酪氨酸中的芳香环设置为联合CH原子__

__\-\[no\]ignh no 忽略坐标文件中的氢原子，因为氢原子的命名规则不统__

__一，有些力场可能无法识别__

__\-\[no\]missing no 当发现坐标文件中的原子有缺失而无法得到成键信息时__

__继续运行。使用此选项存在危险__

__\-\[no\]v no 输出更多屏幕消息__

__\-posrefc <real> 1000 指定位置限制的力常数__

__\-vsite <enum> none 将哪些原子转换为虚拟位点：none，hydrogens，__

__aromatics__

__\-\[no\]heavyh no 增大氢原子的质量__

__\-\[no\]deuterate no 将氢原子的质量增大为2 amu（氘氢）__

__\-\[no\]chargegrp yes 使用 \.rtp ↪ 615 文件中的电荷组__

__\-\[no\]cmap yes 使用cmap扭转（如果 \.rtp ↪ 615 文件中启用）__

__\-\[no\]renum no 对输出的残基重新编号以保证编号连续__

__\-\[no\]rtpres no 使用 \.rtp ↪ 615 条目名称作为残基名称__

#### 6\.4\.65 gmx pme\_error

##### 概要

__gmx pme\_error \[ \-s \[<\.tpr>\] \] \[ \-o \[<\.out>\] \] \[ \-so \[<\.tpr>\] \] \[ \-beta \]  
\[ \-\[no\]tune \] \[ \-self \] \[ \-seed \] \[ \-\[no\]v \]__

##### 说明

__如果使用sPME算法，gmx pme\_error可用于估计静电力的误差。可以使用\-tune 选项指定划分参  
数，以便使误差在实空间和倒易空间两部分的分布相同。粒子自相互作用引起的那部分误差不易计算。  
但一个很好的近似方法是只使用一小部分粒子计算此项，这可以使用\-self选项来指定。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s__

__\[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.out>\] error\.out 通用输出文件__

__\-so \[<\.tpr>\] tuned\.tpr 可选 便携式xdr运行输入文件__

##### 控制选项

##### 选项 默认值 说明

__\-beta <real> \-1 如果为正值，则使用此值覆盖 \.tpr ↪ 619 文件中的ewald\_beta。__

__\-\[no\]tune no 调整划分参数，以使得误差在实空间和倒易空间之间的分布相等__

__\-self <real> 1__

__如果指定值介于0\.0和1\.0之间，则只使用这一比例的带电粒子来__

__确定自相互作用误差__

__\-seed <int> 0__

__当\-self的指定值介于0\.0到1\.0之间时，用于蒙特卡洛算法的__

__随机数种子__

__\-\[no\]v no 显示更多信息__

#### 6\.4\.66 gmx polystat

__gmx polystat \[ \-s \[<\.tpr>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-v \[<\.xvg>\] \] \[ \-p \[<\.xvg>\] \] \[ \-i \[<\.xvg>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-tu \]  
\[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]mw \] \[ \-\[no\]pc \]__

##### 概要

##### 说明

__gmx polystat用于计算聚合物的静态性质与时间的函数关系，并输出其平均值。__

__默认情况下，它会计算聚合物的平均末端距离和回旋半径。程序运行时需要一个索引组，并将其拆分为  
分子。然后使用索引组中每个分子的第一个原子和最后一个原子来确定末端距离。程序会输出总回旋半  
径，以及平均回旋张量的三个主分量。使用\-v 选项可以输出特征向量。使用\-pc选项可以输出各个回  
旋张量的平均特征值。使用\-i选项可以输出内部距离的均方值。__

__使用\-p 选项可以计算持续长度。所选索引组应由聚合物主链上连续成键的原子组成。持续长度根据索  
引编号差值为偶数的键所成夹角的余弦确定，不使用编号差值为奇数的键，因为直链聚合物的主链通常  
全是反式的，因此只能每隔一条键对齐一次。持续长度定义为平均余弦值cos达到1/e时的键数。具体  
数值根据log\(\)的线性插值确定。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] polystat\.xvg xvgr/xmgr文件__

__\-v__

__\[<\.xvg>\] polyvec\.xvg 可选 xvgr/xmgr文件__

__\-p__

__\[<\.xvg>\] persist\.xvg 可选 xvgr/xmgr文件__

__\-i__

__\[<\.xvg>\] intdist\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e \(^0\) 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）  
\-dt 0  
只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧  
之间的时间间隔（默认单位ps）  
\-tu ps 时间的单位：fs，ps，ns，us，ms，s  
\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件  
\-xvg  
xmgrace xvg绘图格式：xmgrace，xmgr，none  
\-\[no\]mw yes 使用质量加权的回旋半径  
\-\[no\]pc no 输出平均特征值__

#### 6\.4\.67 gmx potential

##### 概要

__gmx potential \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-s \[<\.tpr>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-oc \[<\.xvg>\] \] \[ \-of \[<\.xvg>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \]  
\[ \-d \] \[ \-sl \] \[ \-cb \] \[ \-ce \]  
\[ \-tz \] \[ \-\[no\]spherical \] \[ \-ng \] \[ \-\[no\]center \]  
\[ \-\[no\]symm \] \[ \-\[no\]correct \]__

##### 说明

__gmx potential用于计算整个盒子的静电势。计算静电势的方法是，首先将每个切片内的电荷相加，然  
后将得到的电荷分布积分两次。计算时不考虑周期性边界条件。静电势的参考点取为盒子左侧的值。程  
序还可以球坐标中的静电势与r的函数关系，这是通过计算球形切片中的电荷分布并将其积分两次得到  
的。epsilon\_r的值取为 1 ，但在许多情况下使用 2 更合适。__

__选项\-center可以相对于任意组的中心，以绝对盒子坐标进行直方图分格和静电势计算。如果计算的是  
沿Z轴的剖面,相应的盒子维度为bZ，若以整个体系为中心，输出将从\-bZ/2到bZ/2。选项\-symm会  
使得输出关于中心对称,同时也会自动开启\-center。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] potential\.xvg xvgr/xmgr文件__

__\-oc \[<\.xvg>\] charge\.xvg xvgr/xmgr文件__

__\-of \[<\.xvg>\] field\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0 只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-d <string> Z 指定膜的法线方向，X，Y或Z__

__\-sl <int> 10__

__计算静电势与盒子长度的函数关系，将盒子划分为指定数目的__

__切片。__

__\-cb \(^0\) 积分时忽略指定数目的前几个盒子切片  
\-ce 0 积分时忽略指定数目的后几个盒子切片  
\-tz 0 沿盒子方向将所有坐标平移指定的距离  
\-\[no\]spherical no 在球坐标中计算  
\-ng \(^1\) 要考虑的组的个数  
\-\[no\]center no 相对于\(变化\)盒子的中心进行分格\.适用于双层结构\.  
\-\[no\]symm no 随沿轴方向的密度进行对称化,相对于中心\.适用于双层结构\.  
\-\[no\]correct no 假定组的净电荷为零以提高精度__

##### 已知问题

- __积分时忽略一些切片并无必要。如果分子带电，需要指定\-correct选项，否则得到的静电势可  
能线性上升。__

#### 6\.4\.68 gmx principal

##### 概要

__gmx principal \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \]  
\[ \-n \[<\.ndx>\] \] \[ \-a1 \[<\.xvg>\] \] \[ \-a2 \[<\.xvg>\] \]  
\[ \-a3 \[<\.xvg>\] \] \[ \-om \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-\[no\]w \] \[ \-xvg \]  
\[ \-\[no\]foo \]__

##### 说明

__gmx principal用于计算一组原子的三个惯性主轴。注意：旧版本的GROMACS以一种奇怪的转置方  
式输出数据。从GROMACS 5\.0开始，输出文件paxis1\.dat中包含了每一帧的第一个（主要）主轴的  
x/y/z分量，类似的，paxis2\.dat中包含了中间主轴，paxis3\.dat 中包含了最小主轴的x/y/z分量。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构 g96 \+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-a1 \[<\.xvg>\] paxis1\.xvg xvgr/xmgr文件__

__\-a2 \[<\.xvg>\] paxis2\.xvg xvgr/xmgr文件__

__\-a3 \[<\.xvg>\] paxis3\.xvg xvgr/xmgr文件__

__\-om \[<\.xvg>\] moi\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧__

__之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]foo no 哑选项，用于避免空数组__

#### 6\.4\.69 gmx rama

##### 概要

__gmx rama \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-o \[<\.xvg>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \]__

##### 说明

__gmx rama可以从拓扑文件中选择phi/psi二面角（Calpha与酰胺平面的交角）的组合，并计算它们与  
时间的函数关系。使用简单的Unix工具，如grep，你就可以选出特定残基对应的数据。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] rama\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b \(^0\) 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）  
\-e 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）  
\-dt 0  
只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧  
之间的时间间隔（默认单位ps）  
\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件  
\-xvg  
xmgrace xvg绘图格式：xmgrace，xmgr，none__

##### 补充说明

__拉氏图（Ramachandran图）是通过统计蛋白质结构残基的𝜙/𝜓二面角绘制的，集中分布在几个角度范  
围内的区域。物质都具有自发朝能量最低方向变化的特点，自然界的蛋白也是，所以拉氏标准分布图中，  
统计分布密集的区域，对应于蛋白能量低，稳定的构象，在这些区域中，残基侧链彼此间斥力小。模拟  
得到的结果如果绝大多数落在这些范围中，也可以说明具有这样的特征。但分布另一方面也和残基类型  
有关，侧链越小所受的斥力制约越小，在拉氏图中分布范围越广。__

__一些可视化软件可以直接给出拉氏图。在 VMD中，使用VMD Main\->Extensions\->Analysis\-__

__Ramachandran Plot即可得到类似下面的拉氏图。__

#### 6\.4\.70 gmx rdf

##### 概要

__gmx rdf \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-cn \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-fgroup \] \[ \-xvg \]  
\[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \] \[ \-selrpos \]  
\[ \-seltype \] \[ \-bin \] \[ \-norm \] \[ \-\[no\]xy \]  
\[ \-\[no\]excl \] \[ \-cut \] \[ \-rmax \] \[ \-surf \]  
\[ \-ref \] \[ \-sel \]__

##### 说明

__gmx rdf用于计算从一组参考位置（\-ref指定）到一组或多组位置（\-sel指定）的径向分布函数。如  
果要计算相对于\-ref集合中的最近位置的RDF，可以使用\-surf选项：指定后，程序会根据\-surf  
的值将\-ref划分为集合，并使用每个集合中最近的位置。要计算与 z 轴平行的轴周围，处于 x \- y 平  
面内的RDF，可以使用\-xy选项。__

__要设置计算RDF时使用的分格宽度和最大距离，可以使用\-bin和\-rmax选项。后一选项可用于减小  
计算成本，如果对RDF在默认最大距离处的信息不感兴趣的话（使用PBC时，默认最大距离为盒子  
大小的一半，不使用PBC时，默认最大距离为盒子大小的三倍）。__

__要使用拓扑文件（\-s选项）中的排除，可以指定\-excl并确保\-ref和\-sel二者只选择了原子。一  
种更粗略的排除分子内RDF峰的替代方法是，将\-cut选项设置为非零值以清除小距离处的RDF。__

__RDF的归一化因子可以使用：1\)\-ref中的平均位置数（使用\-surf时为组的数目）; 2\)分格的体积；  
3\)该选择的\-sel位置的平均粒子密度。要改变归一化方法，可以使用\-norm选项：__

- __rdf:使用所有因子进行归一化。这会得到常规的RDF。__
- __number\_density:使用前两个因子。这会得到数密度与距离的函数关系。__
- __none:只使用第一个因子。在这种情况下，只使用分格宽度对RDF进行缩放，这样得到的曲线的  
积分代表某一范围内的位置对的个数。__

__注意，排除不影响归一化：即使指定了\-excl，或\-ref和\-sel包含相同的选择，归一化因子仍然是  
NM，而不是N\(M\-排除数\)。__

__对于\-surf选项，提供给\-ref的选区必须对应原子，即不支持质心。此外，此选项暗含了\-nonorm，  
因为分格具有不规则的形状，其体积不易计算。__

__使用\-cn选项可以得到RDF累积数（配位数），即距离r范围内的平均粒子数。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构： tpr ↪^619 ， gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] rdf\.xvg 计算的RDF__

__\-cn \[<\.xvg>\] rdf\_cn\.xvg 可选 累积RDF（配位数）__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时间（默认单位__

__ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的终止时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分__

__析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子（如果未设置，假定为前N个原__

__子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，whole\_mol\_cog，__

__part\_res\_com，part\_res\_cog，part\_mol\_com，__

__part\_mol\_cog，dyn\_res\_com，dyn\_res\_cog，__

__dyn\_mol\_com，dyn\_mol\_cog__

__\-bin <real> 0\.002 分格宽度（单位：nm）__

__\-norm <enum> rdf 归一化方法：rdf，number\_density，none__

__\-\[no\]xy no 只使用距离的x和y分量__

__\-\[no\]excl no 使用拓扑中的排除__

__\-cut \(^0\) 要考虑的最短距离（单位：nm）  
\-rmax \(^0\) 要计算的最大距离（单位：nm）  
\-surf no 相对于参考表面的RDF:no，mol，res  
\-ref 计算RDF的参考选区  
\-sel 计算RDF的选区__

#### 6\.4\.71 gmx report\-methods

##### 概要

__gmx report\-methods \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-m \[<\.tex>\] \] \[ \-o \[<\.out>\] \]__

##### 说明

__gmx report\-methods用于报告由\-s指定的运行输入文件的基本系统信息，报告结果可以直接输出到  
终端，如果运行时指定了\-m 选项会将报告结果输出到LaTeX文件，如果使用了\-o 选项会将报告结  
果输出到无格式的文件中。该功能之前属于 gmx check ↪ 192 。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr__

__用于报告的运行输入文件： tpr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-m__

__\[<\.tex>\]__

__report\.tex 可选 LaTeX格式的报告输出文件__

__\-o__

__\[<\.out>\] report\.out 可选 无格式的报告输出文件__

#### 6\.4\.72 gmx rms

##### 概要

__gmx rms \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \]  
\[ \-f2 \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \] \[ \-o \[<\.xvg>\] \]  
\[ \-mir \[<\.xvg>\] \] \[ \-a \[<\.xvg>\] \] \[ \-dist \[<\.xvg>\] \] \[ \-m \[<\.xpm>\] \]  
\[ \-bin \[<\.dat>\] \] \[ \-bm \[<\.xpm>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-\[no\]w \] \[ \-xvg \]  
\[ \-what \] \[ \-\[no\]pbc \] \[ \-fit \] \[ \-prev \]  
\[ \-\[no\]split \] \[ \-skip \] \[ \-skip2 \] \[ \-max \]  
\[ \-min \] \[ \-bmax \] \[ \-bmin \] \[ \-\[no\]mw \]  
\[ \-nlevels \] \[ \-ng \]__

##### 说明

__gmx rms通过计算均方根偏差（RMSD），尺寸无关的rho相似性参数（rho）或缩放的rho\(rhosc\)来  
比较两个结构，参见Maiorov&Crippen, Proteins __22__ , 273\(1995\)。可使用 \-what选项来选择要计算的参  
数。__

__程序会将轨迹（\-f 指定）中的每个结构与参考结构进行比较。参考结构取自结构文件（\-s 指定）。__

__如果指定了\-mir选项，程序还可以将结构与参考结构的镜像进行比较。这可以作为“显著”值的参考，  
详见Maiorov & Crippen, Proteins __22__ , 273 \(1995\)。__

__使用\-prev选项可以将当前帧的结构与前面指定帧中的结构进行比较。__

__使用\-m 选项可以生成一个 \.xpm ↪ 620 格式的矩阵，其值为轨迹中所有结构彼此之间的对比值。这个矩阵  
文件可使用xv之类的程序可视化，也可以使用 gmx xpm2ps ↪ 363 转换为postscript格式。__

__可以使用\-fit选项控制结构之间的最小二乘叠合方式：完全叠合（旋转和平移），仅平移，或不叠合。__

__选项\-mw控制是否使用质量加权。如果指定了此选项（默认），并提供了一个有效的 \.tpr ↪ 619 文件，程序  
会读取文件中的质量，否则会从GMXLIB 目录下的atommass\.dat文件中获得质量\(已废弃\)。这适用于  
蛋白质，但不一定适用于其他分子。你可以通过指定\-debug选项并查看日志文件来检查是否如此。__

__如果指定了\-f2选项，程序会从第二个轨迹文件中读取“其他结构”，并计算两条轨迹的比较矩阵。__

__使用\-bin选项可以输出比较矩阵的二进制文件。__

__使用\-bm选项可以得到平均键角偏差矩阵，类似于\-m选项。比较时只会考虑对比组中原子之间的键。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr__

__结构\+质量（db）: tpr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-f2 \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] rmsd\.xvg xvgr/xmgr文件__

__\-mir \[<\.xvg>\] rmsdmir\.xvg 可选 xvgr/xmgr文件__

__\-a \[<\.xvg>\] avgrp\.xvg 可选 xvgr/xmgr文件__

__\-dist \[<\.xvg>\] rmsd\-dist\.xvg 可选 xvgr/xmgr文件__

__\-m \[<\.xpm>\] rmsd\.xpm 可选 X PixMap兼容的矩阵文件__

__\-bin \[<\.dat>\] rmsd\.dat 可选 通用数据文件__

__\-bm \[<\.xpm>\] bond\.xpm 可选 X PixMap兼容的矩阵文件__

##### 控制选项

##### 选项 默认值 说明

__\-b \(^0\) 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）  
\-e 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-what <enum> rmsd 结构差异类型：rmsd，rho，rhosc__

__\-\[no\]pbc yes PBC检查__

__\-fit <enum> rot\+trans 叠合到参考结构的方式：rot\+trans，translation，__

__none__

__\-prev <int> 0 与之前的帧进行比较__

__\-\[no\]split no 在时间为零的位置划分图形__

__\-max <real> \-1 比较矩阵中的最大水平__

__\-min <real> \-1 比较矩阵\-skip \(^1\) 每隔指定数目的帧分析一次，即分析帧的间隔  
\-skip2 \(^1\) 每隔指定数目的帧分析一次，即分析帧的间隔__

__中的最小水平__

__\-bmax <real> \-1 键角矩阵中的最大水平__

__\-bmin <real> \-1 键角矩阵中的最小水平__

__\-\[no\]mw yes 叠合时使用质量加权__

__\-nlevels <int> 80 矩阵中的水平数__

__\-ng \(^1\) 计算RMS的组数__

#### 6\.4\.73 gmx rmsdist

##### 概要

__gmx rmsdist \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]__

__\[ \-equiv \[<\.dat>\] \] \[ \-o \[<\.xvg>\] \] \[ \-rms \[<\.xpm>\] \]__

__\[ \-scl \[<\.xpm>\] \] \[ \-mean \[<\.xpm>\] \] \[ \-nmr3 \[<\.xpm>\] \]__

__\[ \-nmr6 \[<\.xpm>\] \] \[ \-noe \[<\.dat>\] \] \[ \-b <time> \] \[ \-e <time> \]__

__\[ \-dt <time> \] \[ \-\[no\]w \] \[ \-xvg <enum> \] \[ \-nlevels <int> \]__

__\[ \-max <real> \] \[ \-\[no\]sumh \] \[ \-\[no\]pbc \]__

##### 说明

__gmx rmsdist用于计算原子距离的均方根偏差，程序的优点在于计算时不需要叠合，而 gmx rms ↪ 309 计  
算标准RMSD时则需要进行叠合。参考结构取自结构文件。t时刻的RMSD定义为参考结构的原子与  
t时刻结构的对应原子之间的距离差值的RMS。  
gmx rmsdist也可用于计算rms距离矩阵，使用平均距离缩放的rms距离，以及使用NMR平均  
（1/r^3和1/r^6平均）的平均距离和矩阵。最后，程序可以生成一个原子对列表，其中包含所有1/r^3  
和1/r^6平均距离小于最大距离（\-max指定，在这种情况下默认为0\.6）的原子对，默认情况下，平均  
是对等价氢原子（所有以\[123\]命名的氢原子三联对）进行的。另外，程序还可以提供等价原子的列  
表（\-equiv 选项），输出文件中每行包含一组等价原子，使用残基编号，残基名称，原子名称指定；如：  
HB 3 SER HB1 3 SER HB2  
残基名称和原子名称必须与结构文件中的名称精确匹配，包括大小写。程序没有规定如何指定非连续的  
原子。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-equiv \[<\.dat>\] equiv\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] distrmsd\.xvg xvgr/xmgr文件__

__\-rms \[<\.xpm>\] rmsdist\.xpm 可选 X PixMap兼容的矩阵文件__

__\-scl \[<\.xpm>\] rmsscale\.xpm 可选 X PixMap兼容的矩阵文件__

__\-mean \[<\.xpm>\] rmsmean\.xpm 可选 X PixMap兼容的矩阵文件__

__\-nmr3 \[<\.xpm>\] nmr3\.xpm 可选 X PixMap兼容的矩阵文件__

__\-nmr6 \[<\.xpm>\] nmr6\.xpm 可选 X PixMap兼容的矩阵文件__

__\-noe \[<\.dat>\] noe\.dat 可选 通用数据文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-nlevels \(^40\) RMS的离散水平数  
\-max \-1 矩阵的最大水平  
\-\[no\]sumh yes 对等价氢原子进行距离平均  
\-\[no\]pbc yes 计算距离时使用周期性边界条件__

#### 6\.4\.74 gmx rmsf

##### 概要

__gmx rmsf \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-q \[<\.pdb>\] \] \[ \-oq \[<\.pdb>\] \] \[ \-ox \[<\.pdb>\] \] \[ \-o \[<\.xvg>\] \]  
\[ \-od \[<\.xvg>\] \] \[ \-oc \[<\.xvg>\] \] \[ \-dir \[<\.log>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]res \]  
\[ \-\[no\]aniso \] \[ \-\[no\]fit \]__

##### 说明

__gmx rmsf用于计算轨迹（\-f选项指定）中原子位置的均方根波动（RMSF，即标准偏差），计算前可  
以先将构型与参考构型（\-s 选项指定）进行叠合（并非必须）。__

__使用\-oq选项可以将RMSF值转换为B因子值，并将其输出到 \.pdb ↪ 614 文件中。默认情况下，此输出  
文件中的坐标来自\-s 选项指定的结构文件，但也可以使用\-q 选项指定另一个 \.pdb ↪ 614 文件，并使用  
其中的坐标。程序几乎不进行错误检查，因此在这种情况下，需要你确保结构文件和 \.pdb ↪ 614 文件中的  
所有原子都完全对应。__

__指定\-ox选项可以将B因子和平均坐标输出到轨迹文件。__

__使用\-od选项可以计算相对于参考结构的均方根偏差。__

__如果指定了 \-aniso选项，gmx rmsf会计算各向异性温度因子U，还会输出平均坐标和含有 ANISOU  
记录的 \.pdb ↪ 614 文件（对应于\-oq或\-ox选项）。注意，U值与取向有关，因此在与实验数据进行比较  
前，请确保已经与实验坐标进行了叠合。__

__当为程序提供了一个 \.pdb ↪ 614 输入文件，并指定了\-aniso选项时，如果 \.pdb ↪ 614 文件中含有任何各向异  
性温度因子，就会生成Uij的相关图。__

__使用\-dir选项可以对平均MSF\(3x3\)矩阵进行对角化。这可用于显示原子最大波动和最小波动的方向。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-q \[<\.pdb>\] eiwit\.pdb 可选 蛋白质数据库文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-oq \[<\.pdb>\] bfac\.pdb 可选 蛋白质数据库文件__

__\-ox \[<\.pdb>\] xaver\.pdb 可选 蛋白质数据库文件__

__\-o \[<\.xvg>\] rmsf\.xvg xvgr/xmgr文件__

__\-od \[<\.xvg>\] rmsdev\.xvg 可选 xvgr/xmgr文件__

__\-oc \[<\.xvg>\] correl\.xvg 可选 xvgr/xmgr文件__

__\-dir__

__\[<\.log>\] rmsf\.log 可选 日志文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧__

__之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]res no 计算每个残基的平均值__

__\-\[no\]aniso no 计算各向异性温度因子__

__\-\[no\]fit yes 计算RMSF之前进行最小二乘叠合。如果不使用这个选项，必须__

__确保参考结构和轨迹匹配。__

#### 6\.4\.75 gmx rotacf

##### 概要

__gmx rotacf \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]d \] \[ \-\[no\]aver \]  
\[ \-acflen \] \[ \-\[no\]normalize \] \[ \-P \]  
\[ \-fitfn \] \[ \-beginfit \] \[ \-endfit \]__

##### 说明

__gmx rotacf用于计算分子的旋转相关函数（ACF）。必须在索引文件中给出原子三联对\(i,j,k\)，由此定  
义两个向量ij和jk。旋转ACF为向量n = ij×jk的自相关函数，即两个向量叉积的自相关函数。由于  
三个原子可张成一个平面，因此三个原子的顺序并不重要。作为可选，通过使用\-d选项，并在索引文  
件中指定原子对\(i，j\)可以计算线性分子的旋转相关函数。__

__示例__

__gmx rotacf \-P 1 \-nparm 2 \-fft \-n index \-o rotacf\-x\-P1 \-fa expfit\-x\-P1 \-beginfit 2\.5  
\-endfit 20\.0__

__上面的命令会使用索引文件中定义的向量间的夹角的一阶Legendre多项式来计算旋转相关函数。并根  
据2\.5 ps到20\.0 ps的数据，将相关函数拟合为双参数指数形式。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 轨迹文件： gro xtc ↪^621 ， trr ↪^619 ， cpt ↪^608 ，__

__↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] rotacf\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

读入轨迹最后一帧的时间，即分析的结束时间（默认单位

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]d no 计算相关函数时使用索引双联对（向量）而不是三联对（平__

__面）__

__\-\[no\]aver yes 对所有分子进行平均__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0__

__用于ACF的Legendre多项式的阶数（ 0 表示不使用）:__

__0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit <real> 0 对相关函数进行指数拟合的起始时间__

__\-endfit <real> \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

#### 6\.4\.76 gmx rotmat

##### 概要

__gmx rotmat \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-\[no\]w \] \[ \-xvg \] \[ \-ref \] \[ \-skip \]  
\[ \-\[no\]fitxy \] \[ \-\[no\]mw \]__

##### 说明

__gmx rotmat用于计算一个构象与参考构象进行最小二乘叠合时所需的旋转矩阵，参考构象由\-s选项  
指定。叠合前会移除平动自由度。输出为三个向量，给出了参考构象x，y和z方向的新方向，例如：  
\(zx, zy, zz\)为轨迹帧中参考z轴的方向。__

__此工具在某些情况下可能会用到，例如，确定界面处分子的取向，轨迹可能由 gmx trjconv \-fit  
rotxy\+transxy产生，移除了 x\-y 平面内的旋转。__

__可以使用\-ref选项指定叠合的参考结构，而不使用\-s选项指定文件中的结构。程序会使用与其他所  
有结构的RMSD之和最小的结构作为参考结构。由于此过程的计算成本正比于帧数的平方，因此\-skip  
选项可用于减少计算成本。程序可以进行完全叠合或只进行 x\-y 平面内的叠合。__

__如果指定了\-fitxy选项，确定旋转矩阵前会先在 x\-y 平面内进行叠合。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] rotmat\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧__

__之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-ref__

__<enum> none 确定最佳参考结构的方式：none，xyz，xy__

__\-skip__

__<int>^1 对\-ref每隔指定数目的帧使用一次__

__\-\[no\]fitxy no 确定旋转矩阵前先进行x/y旋转__

__\-\[no\]mw yes 叠合时使用质量加权__

#### 6\.4\.77 gmx saltbr

##### 概要

__gmx saltbr \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-t \] \[ \-\[no\]sep \]__

##### 说明

__gmx saltbr用于计算所有带电组组合之间的距离与时间的函数关系。这些组可以不同方式组合一起。  
可指定一个最小距离（即截断），这样计算时不会考虑距离从未小于该指定距离的组。__

__程序会输出一些具有固定名称的文件，min\-min\.xvg，plus\-min\.xvg 和 plus\-plus\.xvg，如  
果指定了 \-sep 选项，还会输出每个离子对的文件。在这种情况下，文件名称格式为  
sb\-\(Resname\)\(Resnr\)\-\(Atomnr\)。这种文件的数目可能非常多。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧之__

__间的时间间隔（默认单位ps）__

__\-t \(^1000\) 不考虑距离从未小于此指定距离的组  
\-\[no\]sep no 对每个相互作用使用单独的文件（输出文件可能非常多）__

#### 6\.4\.78 gmx sans

##### 概要

__gmx sans \[ \-s \[<\.tpr>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-d \[<\.dat>\] \] \[ \-pr \[<\.xvg>\] \] \[ \-sq \[<\.xvg>\] \]  
\[ \-prframe \[<\.xvg>\] \] \[ \-sqframe \[<\.xvg>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-tu \] \[ \-xvg \]  
\[ \-bin \] \[ \-mode \] \[ \-mcover \]__

__\[ \-method <enum> \] \[ \-\[no\]pbc \] \[ \-grid <real> \] \[ \-startq <real> \]__

__\[ \-endq <real> \] \[ \-qstep <real> \] \[ \-seed <int> \] \[ \-nt <int> \]__

##### 说明

__gmx sans使用Debye公式计算SANS谱（小角度中子衍射）。目前，使用时需要提供拓扑文件（因为  
需要指定每个原子的元素）。__

__参数：__

__\-pr:计算轨迹平均的归一化g\(r\)函数__

__\-prframe:计算每帧的归一化g\(r\)函数__

__\-sq:计算轨迹平均的SANS强度曲线__

__\-sqframe:计算每帧的SANS强度曲线__

__\-startq:起始q值，单位：1/nm__

__\-endq:终止q值，单位：1/nm__

__\-qstep: q值的步长__

__注意：当使用Debye直接方法时，计算成本正比于1/2 \* N \* \(N \- 1\)，其中N为待研究的组中的原子数。__

__警告：如果指定了\-sq或\-pr，此工具会产生大量文件\!数目最多可达帧数的两倍\!__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-d \[<\.dat>\] nsfactor\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-pr \[<\.xvg>\] pr\.xvg xvgr/xmgr文件__

__\-sq \[<\.xvg>\] sq\.xvg xvgr/xmgr文件__

__\-prframe__

__\[<\.xvg>\] prframe\.xvg 可选 xvgr/xmgr文件__

__\-sqframe__

__\[<\.xvg>\] sqframe\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-bin <real> 0\.2 \[隐藏\]分格宽度（单位：nm）__

__\-mode <enum> direct 计算SANS谱的模式：direct，mc__

__\-mcover <real> \-1 Monte\-Carlo覆盖率，应为\-1（默认值）或\(0，1\]内的数__

__\-method <enum> debye \[隐藏\] SANS谱的计算方法：debye，fft__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-grid <real> 0\.05 \[隐藏\] FFT的格点间距（单位：nm）__

__\-startq <real> 0 起始q值（单位：1/nm）__

__\-endq <real> 2 终止q值（单位：1/nm）__

__\-qstep <real> 0\.01 q值的步长（单位：1/nm）__

__\-seed <int> 0 蒙特卡洛的随机种子__

__\-nt <int> 96 启动的线程数__

#### 6\.4\.79 gmx sasa

##### 概要

__gmx sasa \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-odg \[<\.xvg>\] \] \[ \-or \[<\.xvg>\] \] \[ \-oa \[<\.xvg>\] \]  
\[ \-tv \[<\.xvg>\] \] \[ \-q \[<\.pdb>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-fgroup \]  
\[ \-xvg \] \[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \]  
\[ \-selrpos \] \[ \-probe \] \[ \-ndots \] \[ \-\[no\]prot \]  
\[ \-dgs \] \[ \-surface \] \[ \-output \]__

##### 说明

__gmx sasa用于计算溶剂可及表面积。使用的算法可参考：Eisenhaber F, Lijnzaad P, Argos P, Sander  
C, & Scharf M \(1995\) J\. Comput\. Chem\. __16__ , 273\-284。如果指定了\-q 选项，程序会将Connolly表面  
输出到 \.pdb ↪ 614 文件中，其中节点以原子表示，连接最近节点的边作为CONECT 记录。使用\-odg选项  
可以估算溶剂化自由能，估算时根据每个原子每单位暴露表面积的溶剂化能进行计算。__

__此程序需要使用\-surface选项来指定要计算表面积的组。系统中所有的非溶剂原子都应该包含在内。  
程序始终会计算该组的表面积。作为可选，\-output选项可用于指定其他选区，它应该是整个计算组的  
一部分。这些组的溶剂可及表面积会从整个表面积中抽取出来。__

__程序也可以计算整条轨迹中每个残基（\-or选项）和每个原子（\-oa选项）的表面积的平均值和标准偏  
差（\-or和\-oa选项）。__

__使用\-tv选项可以计算分子的总体积和密度。使用\-pbc选项（默认）时，必须确保分子/表面组不会  
被PBC分开。否则，得到的结果毫无意义。还要考虑在这种情况下正常的探针半径是否合适，或者是  
否要使用其他半径值，如 0 。请记住，体积和密度的计算结果非常粗糙。例如，在冰Ih中，可以很容易  
地将水分子放入孔道中，这样得到的体积过小，而表面积和密度都过大。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构： tpr ↪^619 ， gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] area\.xvg 总面积与时间的函数__

__\-odg__

__\[<\.xvg>\] dgsolv\.xvg 可选 溶剂化自由能估计值与时间的函数__

__\-or \[<\.xvg>\] resarea\.xvg 可选 每个残基的平均面积__

__\-oa \[<\.xvg>\] atomarea\.xvg 可选 每个原子的平均面积__

__\-tv \[<\.xvg>\] volume\.xvg 可选 总体积和密度与时间的函数__

__\-q \[<\.pdb>\] connolly\.pdb 可选 Connolly表面的PDB文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

读入轨迹第一帧的时间，即分析的起始时间（默认单位

__ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的终止时间（默认单__

__位ps）__

__\-dt <time> 0 只使用时刻分析时两帧之间的时间间隔（默认单位t除以dt的余数等于第一帧时间的帧，即ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup <selection> 轨迹文件中存储的原子（如果未设置，假定为前N个__

__原子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，whole\_mol\_cog，__

__part\_res\_com，part\_res\_cog，part\_mol\_com，__

__part\_mol\_cog，dyn\_res\_com，dyn\_res\_cog，__

__dyn\_mol\_com，dyn\_mol\_cog__

__\-probe <real> 0\.14 溶剂探针的半径（单位：nm）__

__\-ndots <int> 24 每个球面的点数，点数越多精度越高__

__\-\[no\]prot yes 将蛋白质也输出到Connolly表面的 \.pdb ↪ 614 文件__

__\-dgs <real> 0 单位面积溶剂化自由能的默认值（kJ/mol/nm^2）__

__\-surface <selection> 要计算表面积的选区__

__\-output <selection> 输出选区补充说明__

#### 6\.4\.80 gmx saxs

##### 概要

__gmx saxs \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-d \[<\.dat>\] \] \[ \-sq \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-xvg \] \[ \-ng \] \[ \-startq \]  
\[ \-endq \] \[ \-energy \]__

##### 说明

__gmx saxs根据Cromer方法计算指定索引组的SAXS结构因子。计算时需要拓扑和轨迹文件。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-d \[<\.dat>\] sfactor\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-sq \[<\.xvg>\] sq\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e \(^0\) 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）  
\-dt 0  
只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时  
两帧之间的时间间隔（默认单位ps）  
\-xvg xmgrace xvg绘图格式：xmgrace，xmgr，none  
\-ng \(^1\) 要计算SAXS的组数  
\-startq 0 起始q值（单位：1/nm）  
\-endq 60 终止q值（单位：1/nm）  
\-energy 12 入射X射线的能量（keV）__

#### 6\.4\.81 gmx select

##### 概要

__gmx select \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-os \[<\.xvg>\] \] \[ \-oc \[<\.xvg>\] \] \[ \-oi \[<\.dat>\] \]  
\[ \-on \[<\.ndx>\] \] \[ \-om \[<\.xvg>\] \] \[ \-of \[<\.xvg>\] \]  
\[ \-ofpdb \[<\.pdb>\] \] \[ \-olt \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-fgroup \]  
\[ \-xvg \] \[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \]  
\[ \-selrpos \] \[ \-seltype \] \[ \-select \]  
\[ \-\[no\]norm \] \[ \-\[no\]cfnorm \] \[ \-resnr \]  
\[ \-pdbatoms \] \[ \-\[no\]cumlt \]__

##### 说明

__gmx select用于输出与动态选区相关的基本数据。它可用于一些简单的分析，其输出也可以与其他程  
序和/或外部分析程序的输出组合起来，用以计算更复杂的数据。可以使用gmx help selections获取  
选区语法的详细帮助。__

__输出选项可以任意组合，但要注意\-om选项只对第一个选区进行操作。还要注意，如果没有指定任何输  
出选项，则不会生成任何输出。__

__指定\-os选项时会逐帧计算每个选区中的位置数。指定\-norm选项时，输出值会介于 0 和 1 之间，代  
表相对于最大位置数的比例（例如，对于选区resname RA and x < 5，最大位置数就是RA残基中的  
原子数）。指定\-cfnorm选项时，（\-os文件）输出值会除以选区涵盖（全局位置数）的比例。\-norm  
和\-cfnorm选项可以彼此独立地指定。__

__指定\-oc选项时，会输出每个选区的覆盖比例与时间的函数。__

__指定\-oi选项时，会输出选中的原子/残基/分子与时间的函数。输出中，第一列为帧时间，第二列为位  
置数，后续列为原子/残基/分子编号。如果指定的选区数大于 1 ，则第二组的位置数紧邻第一组的最后  
一个数字输出，依此类推。__

__指定\-on选项时，会将选中原子输出为索引文件，此文件与make\_ndx和分析工具兼容。每个选区会__

##### 输出为一个选区组，对于动态选区，每帧都会输出一个组。

__要得到残基编号，可以指定\-resnr选项控制\-oi的输出：number（默认）会输出残基在输入文件中  
的编号，而index则会按照残基在输入文件中的出现顺序，从 1 开始，为残基指定唯一编号并输出。前  
者更直观，但如果输入中包含多个具有相同编号的残基，得到的输出就没那么有用了。__

__指定\-om选项时，会输出第一选区的掩码与时间的函数。输出中的每一行对应一帧，为每个可能被选中  
的原子/残基/分子指定 0 或 1 。 1 表示该原子/残基/分子在当前帧中被选中， 0 表示未选中。__

__指定\-of选项时，会输出每个位置的占据比例（即该位置被选中的帧所占的比例）。__

__指定\-ofpdb选项时，会输出一个PDB文件，其中占据率列的值为选区中每个原子的占据比例。PDB  
文件中的坐标来自输入拓扑的坐标。\-pdbatoms选项可用于控制哪些原子会出现在输出的PDB文件中：  
all会输出所有原子，maxsel 会输出所有可能被选中的原子，selected会输出至少在一帧中被选中  
的原子。__

__指定\-olt选项时，会输出一个直方图，显示了选中位置数与位置持续被选中时间的函数关系。\-cumlt  
选项可用于控制是否在直方图中包含较长间隔的子间隔。__

__\-om，\-of和\-olt选项只适用于动态选区。__

__要得到选区的坐标，可以使用 gmx trajectory ↪ 340 。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 输入结构： tpr ↪^619 ， gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-os \[<\.xvg>\] size\.xvg 可选 每个选择中的位置数__

__\-oc \[<\.xvg>\] cfrac\.xvg 可选 每个选区的覆盖比例__

__\-oi \[<\.dat>\] index\.dat 可选 每个选区所选中的索引__

__\-on \[<\.ndx>\] index\.ndx 可选 由选区生成的索引文件__

__\-om \[<\.xvg>\] mask\.xvg 可选 被选中位置的掩码__

__\-of \[<\.xvg>\] occupancy\.xvg 可选 被选中位置的占据比例__

__\-ofpdb__

__\[<\.pdb>\] occupancy\.pdb 可选 含有被选中位置占据比例的PDB文件__

__\-olt \[<\.xvg>\] lifetime\.xvg 可选 寿命直方图__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时间（默认单位__

__ps）__

__\-e <time> 0__

读入轨迹最后一帧的时间，即分析的终止时间（默认单位

__ps）__

__\-dt <time> 0 只使用时刻t除以dt的余数等于第一帧时间的帧，即分__

__析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子（如果未设置，假定为前N个原__

__子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，whole\_mol\_cog，__

__part\_res\_com，part\_res\_cog，part\_mol\_com，__

__part\_mol\_cog，dyn\_res\_com，dyn\_res\_cog，__

__dyn\_mol\_com，dyn\_mol\_cog__

__\-select__

__<selection> 要分析的选区__

__\-\[no\]norm no 指定\-os选项时，用总位置数进行归一化__

__\-\[no\]cfnorm no 指定\-os选项时，用覆盖比例进行归一化__

__\-resnr <enum> number 指定\-oi和\-on选项时，残基编号的输出方式：__

__number，index__

__\-pdbatoms <enum> all 指定\-ofpdb选项时，要输出的原子：all，maxsel，__

__selected__

__\-\[no\]cumlt yes 指定\-olt选项时，累积时计入较长间隔的子间隔__

#### 6\.4\.82 gmx sham

##### 概要

__gmx sham \[ \-f \[<\.xvg>\] \] \[ \-ge \[<\.xvg>\] \] \[ \-ene \[<\.xvg>\] \] \[ \-dist \[<\.xvg>\] \]  
\[ \-histo \[<\.xvg>\] \] \[ \-bin \[<\.ndx>\] \] \[ \-lp \[<\.xpm>\] \]  
\[ \-ls \[<\.xpm>\] \] \[ \-lsh \[<\.xpm>\] \] \[ \-lss \[<\.xpm>\] \]  
\[ \-ls3 \[<\.pdb>\] \] \[ \-g \[<\.log>\] \] \[ \-\[no\]w \] \[ \-xvg \]  
\[ \-\[no\]time \] \[ \-b \] \[ \-e \] \[ \-ttol \]__

__\[ \-n <int> \] \[ \-\[no\]d \] \[ \-\[no\]sham \] \[ \-tsham <real> \]__

__\[ \-pmin <real> \] \[ \-dim <vector> \] \[ \-ngrid <vector> \]__

__\[ \-xmin <vector> \] \[ \-xmax <vector> \] \[ \-pmax <real> \]__

__\[ \-gmax <real> \] \[ \-emin <real> \] \[ \-emax <real> \]__

__\[ \-nlevels <int> \]__

##### 说明

__gmx sham用于计算多维的自由能，焓和熵。gmx sham会读入一个或多个 \.xvg ↪ 623 文件并分析数据集。  
gmx sham的基本功能是利用Boltzmann反演多维直方图方法（\-lp 选项）计算吉布斯自由能形貌图  
（\-ls选项），但也可计算焓（\-lsh选项）和熵（\-lss选项）的形貌图。程序可以计算用户提供的任  
何数据的直方图。输入文件中每行的第一个数据可以是时间（见\-time选项），后面跟着任意数目的 y  
值。当使用&（\-n 选项）隔开时，可以读入多个数据集，在这种情况下，每行只会读取一个 y 值。程  
序会忽略所有以\#和@开头的行。  
当系综并非Boltzmann系综，但又需要使用自由能进行偏置时，可以使用\-ge选项指定这个自由能的  
文件。\-f指定的输入文件中每个（多维）数据点都需要一个自由能数值。  
可以使用\-ene选项指定一个能量文件。在使用Kumar等人的单直方图分析方法时，这些能量可用作  
权重函数。如果提供了温度（处于文件中的第二列），会应用实验加权方案。此外，这些值还会用于计算  
焓和熵。  
可以使用\-dim选项指定距离的维数。当距离为 2 维或 3 维时，两个粒子采样的圆周或表面会随距离的  
增加而增加。根据想要展示的内容，可以选择是否校正直方图和自由能的体积效应。对 2 维和 3 维，概  
率可分别使用r和r^2进行归一化。可以使用\-1来指示两个向量间的夹角（单位：度）:使用角度的正  
弦进行归一化。注意，对两个向量间的夹角，使用内积或余弦是自然的，因为它可以产生相同体积的分  
格。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xvg>\] graph\.xvg xvgr/xmgr文件__

__\-ge \[<\.xvg>\] gibbs\.xvg 可选 xvgr/xmgr文件__

__\-ene__

__\[<\.xvg>\] esham\.xvg 可选 xvgr/xmgr文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-dist \[<\.xvg>\] ener\.xvg 可选 xvgr/xmgr文件__

__\-histo__

__\[<\.xvg>\] edist\.xvg 可选 xvgr/xmgr文件__

__\-bin \[<\.ndx>\] bindex\.ndx 可选 索引文件__

__\-lp \[<\.xpm>\] prob\.xpm 可选 X PixMap兼容的矩阵文件__

__\-ls \[<\.xpm>\] gibbs\.xpm 可选 X PixMap兼容的矩阵文件__

__\-lsh \[<\.xpm>\] enthalpy\.xpm 可选 X PixMap兼容的矩阵文件__

__\-lss \[<\.xpm>\] entropy\.xpm 可选 X PixMap兼容的矩阵文件__

__\-ls3 \[<\.pdb>\] gibbs3\.pdb 可选 蛋白质数据库文件__

__\-g \[<\.log>\] shamlog\.log 可选 日志文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]time yes 输入数据的第一列为时间__

__\-b <real> \-1 读取数据集的起始时间__

__\-e <real> \-1 读取数据集的终止时间__

__\-ttol <real> 0 时间的容差，合适的单位（通常为ps）__

__\-n <int> 1__

__读取的数据集的数目，不同数据集之间以只含&的行进行__

__分隔__

__\-\[no\]d no 使用导数__

__\-\[no\]sham yes 即使提供能量，也不使用能量加权__

__\-tsham <real> 298\.15 用于单直方图分析的温度__

__\-pmin <real> 0 最小概率。小于此值的任何值都设置为零__

__\-dim <vector> 1 1 1__

__计算距离所用的维数，用于体积校正（最多 3 个值，大于 3__

__的维度其值与维度 3 相同__）

__\-ngrid__

__<vector> 32 32 32__

__能量形貌的分格数（最多 3 个值，大于 3 的维度其值与维__

__度 3 相同）__

__\-xmin <vector> 0 0 0 能量形貌图中轴的最小值（维度大于 3 时，见上文）__

__\-xmax <vector> 1 1 1 能量形貌图中轴的最大值（维度大于 3 时，见上文）__

__\-pmax <real> 0 输出概率的最大值，默认为计算值__

__\-gmax <real> 0 输出自由能的最大值，默认为计算值__

__\-emin <real> 0 输出焓的最小值，默认为计算值__

__\-emax \(^0\) 输出焓的最大值，默认为计算值  
\-nlevels \(^25\) 能量形貌图的水平数__

#### 6\.4\.83 gmx sigeps

##### 概要

__gmx sigeps \[ \-o \[<\.xvg>\] \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-c6 \]  
\[ \-cn \] \[ \-pow \] \[ \-sig \] \[ \-eps \]  
\[ \-A \] \[ \-B \] \[ \-C \] \[ \-qi \]  
\[ \-qj \] \[ \-sigfac \]__

##### 说明

__gmx sigeps是一个简单的工具，可以将C6/C12或C6/Cn组合转换成sigma和epsilon，或者反过来。  
它还可以将势能输出到文件中。此外，它还可以将Buckingham势近似地转化为Lennard\-Jones势。__

##### 选项

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] potje\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-c6 <real> 0\.001 C6__

__\-cn <real> 1e\-06 排斥项常数__

__\-pow <int> 12 排斥项的次数__

__\-sig <real> 0\.3 sigma__

__\-eps <real> 1 epsilon__

__\-A <real> 100000 Buckingham势的A__

__\-B <real> 32 Buckingham势的B__

__\-C <real> 0\.001 Buckingham势的C__

__\-qi <real> 0 粒子i的电荷qi__

__\-qj <real> 0 粒子j的电荷qj__

__\-sigfac <real> 0\.7 输出时，sigma前的因子__

#### 6\.4\.84 gmx solvate

##### 概要

__gmx solvate \[ \-cp \[<\.gro/\.g96/\.\.\.>\] \] \[ \-cs \[<\.gro/\.g96/\.\.\.>\] \]  
\[ \-p \[<\.top>\] \] \[ \-o \[<\.gro/\.g96/\.\.\.>\] \] \[ \-box \]  
\[ \-radius \] \[ \-scale \] \[ \-shell \]  
\[ \-maxsol \] \[ \-\[no\]vel \]__

##### 说明

__gmx solvate有两个功能：  
1\)生成一个填充满溶剂的盒子。可以通过指定\-cs和\-box选项来完成。或者，对具有盒子信息但不  
含原子的结构文件，可以通过指定\-cs和\-cp选项来实现。  
2\)将溶质分子，如蛋白质进行溶剂化，使其处于溶剂分子的包围中。可以通过指定\-cp（溶质）和\-cs  
（溶剂）选项来完成。如果没有指定\-box选项，会使用溶质坐标文件（\-cp）中的盒子信息。如果希望  
将溶质置于盒子中心，可以使用 gmx editconf ↪ 231 命令，它有复杂的选项用于更改盒子的尺寸以及居中溶  
质分子。对某一位置，如果溶质分子中的任意原子与溶剂分子中的任意原子之间的距离小于这两个原子  
的缩放范德华半径之和，会移除盒子中的溶剂分子。程序会读取数据文件（vdwradii\.dat）中的范德  
华半径，并根据\-scale选项指定的值对其进行缩放。如果无法在数据文件中找到所需的半径值，相应  
的原子会使用\-radius选项指定的（未缩放）距离。注意，这些半径在使用时是根据原子名称确定的，  
因此不同力场之间的区别很大。  
默认使用的溶剂是简单点电荷水模型（SPC，Simple Point Charge），坐标文件来自$GMXLIB/spc216\.  
gro。这个坐标文件也可用于其他的 3 位点水模型，因为经过短时间的平衡就可以消除这些模型之间的  
微小差异。程序也支持其他的溶剂以及混合溶剂。对溶剂类型的唯一限制是一个溶剂分子只能包含一种  
残基。程序会使用坐标文件中的残基信息，因此应保持一定程度的一致性。实践中，这意味着溶剂坐标  
文件中的两个连续的溶剂分子应具有不同的残基编号。溶质盒子是根据坐标文件中的坐标堆叠构建而成  
的。这意味着这些坐标应在周期性边界条件下进行平衡，以确保分子在堆叠界面上排列良好。可以使用  
\-maxsol选项指定填充的溶剂分子的最大数目，程序只会填充前\-maxsol个溶剂分子而忽略其他本可  
以填充进盒子的溶剂分子。这样做可能会在盒子中形成一部分真空，并导致以后模拟时出现问题。请明  
智地选择盒子体积。  
如果\-shell选项的指定值大于零，程序会在溶质周围放置指定厚度（单位：nm）的水层。提示：最好  
先将蛋白质置于盒子中心（使用 gmx editconf ↪ 231 ）。  
最后，作为可选功能，gmx solvate还可以删除拓扑文件中一些行，这些行给出了已添加的溶剂分子数  
目的信息，并在坐标文件中添加包含溶剂分子总数的新行。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-cp \[<\.gro/\.g96/\.\.\.>\] protein\.gro 可选 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，__

__brk，ent，esp tpr ↪ 619__

__\-cs \[<\.gro/\.g96/\.\.\.>\] spc216\.gro 库 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，__

__brk，ent，esp tpr ↪ 619__

##### 输入/输出文件选项

##### 选项 默认文件 类型 说明

__\-p__

__\[<\.top>\] topol\.top 可选 拓扑文件__

__输出文件选项__

##### 选项 默认文件 类型 说明

__\-o \[<\.gro/\.g96/\.\.\.>\] out\.gro__

__结构文件： gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，brk，__

__ent，esp__

##### 控制选项

##### 选项 默认值 说明

__\-box <vector> 0 0 0 盒子尺寸（单位：nm）__

__\-radius <real> 0\.105 默认的范德华距离（单位：nm）__

__\-scale <real> 0\.57__

__用于数据文件share/gromacs/top/vdwradii\.dat中范德华半__

__径的缩放因子。对水中的蛋白质，使用默认值0\.57得到的密度__

__接近1000 g/l。__

__\-shell \(^0\) 溶质周围可选水层的厚度  
\-maxsol 0__

__如果可以填充进盒子中，要添加的溶剂分子的最大数目。若为零__

__（默认值），则忽略此选项__

__\-\[no\]vel no 保持输入文件中溶质和溶剂分子的速度__

##### 已知问题

##### • 初始构型中所有分子必须保持完整。

##### 补充说明

__gmx solvate可以为模拟分子添加溶剂环境。__

- __\-cp:带盒子参数的分子坐标文件，一般是gmx editconf的输出文件__
- __\-cs:添加的水分子模型，如spc216，spce，tip3p，tip4p等__
- __\-o:输出坐标文件，就是添加水分子之后的分子坐标文件，默认为\.gro文件，但也可以为其他格  
式，如pdb__
- __\-p:体系拓扑文件，gmx solvate会往里面写入添加水分子的个数。这个不要忘记，不然在进行  
下一步计算时，会出现坐标文件和拓扑文件中原子数不一致的错误__

__添加水分子后需要用VMD等软件查看结果，因为有时产生的构型不尽合理。若发现某一水分子出现在  
蛋白结构中，而此位置本来不希望有水分子存在，那么可以找出这个水分子的残基标号，进行删除，同  
时减少拓扑文件中水分子的数目。__

__使用范例__

- __\-box a b c:空盒子__
- __\-cs slv\.gro \-box a b c:以slv\.gro中分子填充盒子，可以使用\-maxsol N__
- __\-cp slu\.gro \-box a b c:指定盒子，否则使用slu\.gro的盒子__
- __\-cp slu\.gro \-cs slv\.gro:以slv填充slu的盒子__
- __\-cp slu\.gro \-cs slv\.gro \-shell a b:表面填充__
- __\-cp slu\.gro \-cs slv\.gro \-maxsol N \-box a b c__

#### 6\.4\.85 gmx sorient

##### 概要

__gmx sorient \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-no \[<\.xvg>\] \] \[ \-ro \[<\.xvg>\] \]  
\[ \-co \[<\.xvg>\] \] \[ \-rc \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]com \] \[ \-\[no\]v23 \]  
\[ \-rmin \] \[ \-rmax \] \[ \-cbin \]  
\[ \-rbin \] \[ \-\[no\]pbc \]__

##### 说明

__gmx sorient用于分析溶质分子周围的溶剂分子的取向。它可以计算从一个或多个参考位置到每个溶剂  
分子的第一个原子的向量（A）与另外两个向量之间的夹角：__

- __theta\_1:向量A与从溶剂分子的第一个原子到第二和第三个原子中点的向量之间的夹角。__
- __theta\_2:向量A与由三个原子定义的溶剂分子平面的法线之间的夹角，或者，如果指定了\-v23  
选项，向量A与从原子 2 和到原子 3 的向量之间的夹角。__

__参考位置可以是一组原子或一组原子的质心。溶剂原子组中的每个溶剂分子只能包含 3 个原子。对每一  
帧，\-o和\-no选项指定的文件中只会输出处于\-rmin和\-rmax之间的溶剂分子。__

__\-o: rmin<=r<=rmax范围内cos\(theta\_1\)的分布。  
\-no: rmin<=r<=rmax范围内cos\(theta\_2\)的分布  
\-ro: <cos\(theta\_1\)>和<3cos^2\(theta\_2\)\-1>与距离的函数。  
\-co:对处于距离r范围内所有溶剂分子的cos\(theta\_1\)和3cos^2\(the2\_2\-1\)进行加和，得到各自与r  
的函数关系。__

__\-rc:溶剂分子的分布与r的函数关系__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构 g96 \+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] sori\.xvg xvgr/xmgr文件__

__\-no \[<\.xvg>\] snor\.xvg xvgr/xmgr文件__

__\-ro \[<\.xvg>\] sord\.xvg xvgr/xmgr文件__

__\-co \[<\.xvg>\] scum\.xvg xvgr/xmgr文件__

__\-rc \[<\.xvg>\] scount\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两__

__帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]com no 使用质心作为参考位置__

__\-\[no\]v23 no 使用原子 2 和 3 之间的向量__

__\-rmin \(^0\) 最小距离（单位：nm）  
\-rmax 0\.5 最大距离（单位：nm）  
\-cbin 0\.02 余弦的分格宽度  
\-rbin 0\.02 距离r的分格宽度（单位：nm）  
\-\[no\]pbc no 计算质心时检查PBC。只有当参考组包含多个分子时才需要使  
用此选项。__

##### 补充说明

##### 此程序特别适用于计算溶质分子周围水分子的角度分布。

__设溶质为单原子离子或分子质心Ref，溶剂为水分子原子 1 为O，原子 2 和 3 为H，则𝜃 1 对应Ref至  
O的向量𝐴 =⃗ 𝑅⃗𝑅𝑒𝑓−𝑅⃗𝑂与O至两个H连线中点的向量𝑅⃗OH2\+ 2 𝑅⃗OH3之间的夹角，后一向量的方向与  
水分子偶极矩的方向相同。因此，𝜃 1 可视为溶质分子周围水分子偶极矩的取向。𝜃 2 对应𝐴⃗与水分子平  
面法线的夹角。当使用\-v23选项时，则为𝐴⃗与两个H连线𝑅⃗H3−𝑅⃗H2之间的夹角。__

#### 6\.4\.86 gmx spatial

##### 概要

__gmx spatial \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-\[no\]w \] \[ \-\[no\]pbc \]  
\[ \-\[no\]div \] \[ \-ign \] \[ \-bin \] \[ \-nab \]__

##### 说明

__gmx spatial用于计算空间分布函数（SDF），其输出文件为Gaussian98 cube格式，可使用VMD读  
取。对于含有32,000个原子和运行了50 ns的轨迹，计算SDF大约需要 30 分钟，其中大部分时间都用  
于运行两次trjconv，因为需要使用它对系统进行正确的居中。计算时也需要很多空间（会产生轨迹文  
件的 3 个副本）。尽管如此，如果使用了正确的叠合选区，得到的结果非常漂亮，且含有丰富信息。程序  
可以处理运动范围很广的组中的3\-4个原子（如溶液中的游离氨基酸），也可以选择稳定折叠结构的蛋  
白质骨架，计算溶剂分子的SDF，得到时间平均的溶剂化壳层。这个程序也可用于计算任意笛卡尔坐标  
的SDF。为此，只要忽略前面的 gmx trjconv ↪ 343 步骤即可。__

__使用方法：为得到有意义的SDF，整个轨迹中溶质分子必须在盒子内居中，并去除其平动和转动。也就  
是说，统计周围分子的SDF时必须基于相对固定的参考坐标系。为此，可能需要使用gmx trjconv对轨  
迹进行多次处理。此外，可能还需要定义特殊的分析组，并使用\-n选项传递给gmx trjconv。__

__1\.使用 gmx make\_ndx ↪ 270 创建两个组，一个包含中心分子，一个包含要统计SDF的原子__

__2\.使中心分子在盒子内居中，同时所有其他分子处于盒子内gmx trjconv \-s a\.tpr \-f a\.tng \-o__

__b\.tng \-boxcenter tric \-ur compact \-pbc none__

__3\.gmx trjconv \-s a\.tpr \-f b\.tng \-o c\.tng \-fit rot\+trans  
4\.使用第三步得到的输出文件c\.tng 运行gmx spatial  
5\.使用VMD或其他软件载入得到的grid\.cube文件，以等值面模式查看结果。__

__注意，对一些系统，如胶束系统，在步骤 1 和步骤 2 之间可能还需要运行gmx trjconv \-pbc cluster。__

##### 警告

__生成的SDF cube文件中包含了具有非零占据的所有分格。但是，前面的 gmx trjconv ↪ 343 使用了\-fit  
rot\+trans选项，意味着系统将会在空间中进行旋转和平移（所选的组不会）。因此，返回值只在所选  
中心组/坐标周围的一定区域内有意义，在整个轨迹中，这些区域与平移/旋转后的系统之间存在完全重  
叠。请确保能满足这一条件。__

##### 激进选项

__为减少计算所需的空间和时间，可以只输出运行 gmx trjconv ↪ 343 所需的坐标。但是，请确保\-nab选项  
的指定值足够高，因为程序会根据初始坐标和\-nab选项的值分配立方体分格所需的内存。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧之__

__间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-\[no\]pbc no 计算距离时使用周期性边界条件__

__\-\[no\]div yes 根据原子/最小立方体尺寸计算并应用分格占据的因子。指定用于可__

__视化，不指定（\-nodiv）可得到每帧的准确计数__

__\-ign <int> \-1 不显示的外部立方体的数目（正值可能会减少边界斑点；\-1可保证__

__保外部表面可见）__

__\-bin__

__<real> 0\.05 分格宽度（单位：nm）__

__\-nab \(^16\) 附加的分格数目，用于保证分配的内存足够大__

##### 已知问题

__• 当分配的内存不足时，可能会出现段错误。程序通常会检测这一错误，并在出错前终止，同时给出__

__警告消息，建议使用\-nab选项（附加分格数）或增加其值。但是，程序并不能检测到所有此类事__

__件。如果遇到段错误，请试着增加\-nab值再次运行程序。__

__如果得到的SDF等值面不够光滑，请增加轨迹的帧数，并检查\-bin的指定值时是否合适。__

__此程序计算SDF的方式不够高效。如果体系含有多个中心分子类型，则每帧可使用每个中心分子  
进行居中，得到更多的统计结果。__

#### 6\.4\.87 gmx spol

##### 概要

__gmx spol \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-dt \] \[ \-\[no\]w \]  
\[ \-xvg \] \[ \-\[no\]com \] \[ \-refat \] \[ \-rmin \]  
\[ \-rmax \] \[ \-dip \] \[ \-bw \]__

##### 说明

__gmx spol用于分析溶质分子周围的偶极，特别适用于极化水模型。程序计算时需要一组参考原子或参  
考质心（\-com选项），以及一组溶剂原子。程序会先将溶剂原子组划分为分子。然后确定每一溶剂分子  
到参考组原子或其质心的最近距离。并给出这些距离的累积分布。对处于\-rmin和\-rmax之间的每一  
距离，程序会计算距离向量与溶剂分子偶极的内积。对于带有净电荷的溶剂分子（离子），程序会从每一  
所选离子的所有原子中均匀地减去离子的净电荷。程序会输出这些偶极分量的平均值。对极化的处理类  
似，并会从瞬时偶极中减去平均偶极。平均偶极的大小由\-dip选项指定，方向由所选溶剂组中的第一  
个原子到第二个和第三个原子连线中点的向量定义。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.xvg>\] scdist\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b \(^0\) 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）  
\-e 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）  
\-dt 0  
只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两  
帧之间的时间间隔（默认单位ps）  
\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件  
\-xvg xmgrace xvg绘图格式：xmgrace，xmgr，none  
\-\[no\]com no 使用质心作为参考位置__

__\-refat \(^1\) 溶剂分子的参考原子  
\-rmin \(^0\) 最大距离（单位：nm）  
\-rmax 0\.32 最大距离（单位：nm）  
\-dip 0 平均偶极（单位：D）  
\-bw 0\.01 分格宽度（单位：nm）__

#### 6\.4\.88 gmx tcaf

##### 概要

__gmx tcaf \[ \-f \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-ot \[<\.xvg>\] \] \[ \-oa \[<\.xvg>\] \] \[ \-o \[<\.xvg>\] \] \[ \-of \[<\.xvg>\] \]  
\[ \-oc \[<\.xvg>\] \] \[ \-ov \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]mol \] \[ \-\[no\]k34 \]  
\[ \-wt \] \[ \-acflen \] \[ \-\[no\]normalize \] \[ \-P \]  
\[ \-fitfn \] \[ \-beginfit \] \[ \-endfit \]__

##### 说明

__gmx tcaf用于计算横向电流自相关（TCAF，tranverse current autocorrelation Function）。它们可用  
于估算剪切粘度𝜂。详细信息请参考：Palmer, Phys\. Rev\. E __49__ \(1994\) pp 359\-366。__

__程序计算横向电流时会使用k向量\(1,0,0\)和\(2,0,0\)，它们同时也处于 y 和 z 方向；程序也会使用  
\(1,1,0\)和\(1,\-1,0\)向量，它们同时也处于另外 2 个平面（这些向量并不独立）;程序还会使用\(1,1,1\)向  
量以及其他三个盒子体对角线方向（它们也不独立）。对每个k向量，程序会使用正弦和余弦，以及 2  
个垂直方向上的速度。这样总共有1622=64个横向电流。对每个k向量会计算并拟合一次自相关，这  
就得到了 16 个TCAF。每个TCAF会拟合为f\(t\) = exp\(\-v\)\(cosh\(Wv\) \+ 1/W sinh\(Wv\)\)，其中v =  
\-t/\(2 tau\)，W = sqrt\(1 \- 4 tau eta/rho k^2\)，这样得到了 16 个tau和eta值。拟合权重随时间指数  
衰减exp\(\-t/w\)，时间常数为w\(\-wt选项指定\)，计算TCAF与拟合的时间为5\*w。𝜂的值应该拟合为  
1\-eta\(k\)k^2，从中就可以估算出k=0时的剪切粘度。__

__当选用立方体盒子时，可以指定\-oc选项，这样TCAF可以对所有长度相同的k向量进行平均。得到  
的TCAF也更准确。立方TCAF和拟合结果都会输出到\-oc指定的文件，立方eta估计值会输出到  
\-ov指定的文件。__

__如果指定了\-mol选项，程序会根据分子而不是原子来计算横向电流。在这种情况下，索引组应该由分  
子编号而不是原子编号组成。__

__要获得无限波长时的粘度，\-ov指定的文件中依赖于k的粘度应根据eta\(k\) = eta\_0 \(1 \- a k^2\)进行  
拟合。__

__注意：请确保坐标和速度的输出频率足够高。自相关函数起始的非指数部分对于得到好的拟合结果非常  
重要。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.trr/\.cpt/\.\.\.>\] traj\.trr 全精度轨迹文件： trr ↪ 619 ， cpt ↪ 608 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选 结构 g96 \+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ot \[<\.xvg>\] transcur\.xvg 可选 xvgr/xmgr文件__

__\-oa \[<\.xvg>\] tcaf\_all\.xvg xvgr/xmgr文件__

__\-o \[<\.xvg>\] tcaf\.xvg xvgr/xmgr文件__

__\-of \[<\.xvg>\] tcaf\_fit\.xvg xvgr/xmgr文件__

__\-oc \[<\.xvg>\] tcaf\_cub\.xvg 可选 xvgr/xmgr文件__

__\-ov \[<\.xvg>\] visc\_k\.xvg xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]mol no 计算分子的TCAF__

__\-\[no\]k34 no 也使用k=\(3,0,0\)和k=\(4,0,0\)__

__\-wt <real> 5 TCAF拟合权重的指数衰减时间__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0__

__用于ACF的Legendre多项式的阶数（ 0 表示不使用）:__

__0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit <real> 0 对相关函数进行指数拟合的起始时间__

__\-endfit <real> \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

#### 6\.4\.89 gmx traj

##### 概要

__gmx traj \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-ox \[<\.xvg>\] \] \[ \-oxt \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-ov \[<\.xvg>\] \]  
\[ \-of \[<\.xvg>\] \] \[ \-ob \[<\.xvg>\] \] \[ \-ot \[<\.xvg>\] \] \[ \-ekt \[<\.xvg>\] \]  
\[ \-ekr \[<\.xvg>\] \] \[ \-vd \[<\.xvg>\] \] \[ \-cv \[<\.pdb>\] \] \[ \-cf \[<\.pdb>\] \]  
\[ \-av \[<\.xvg>\] \] \[ \-af \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-tu \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]com \]  
\[ \-\[no\]pbc \] \[ \-\[no\]mol \] \[ \-\[no\]nojump \] \[ \-\[no\]x \] \[ \-\[no\]y \]  
\[ \-\[no\]z \] \[ \-ng \] \[ \-\[no\]len \] \[ \-\[no\]fp \] \[ \-bin \]  
\[ \-ctime \] \[ \-scale \]__

##### 说明

__gmx traj用于输出坐标，速度，力和/或盒子。使用\-com选项可以计算各个组质心的坐标，速度和力。  
如果指定了\-mol选项，程序会将索引文件中的数字视为分子编号，并对每个分子使用与\-com选项相  
同的过程。__

__如果轨迹文件中存在速度信息，使用\-ot选项可以输出每个组的温度。注意，计算时没有对约束自由度  
进行修正\!此选项暗含了\-com选项。__

__如果轨迹文件中存在速度信息，指定了\-ekt和\-ekr选项可以输出每个组的平动能和转动能。此选项  
暗含了\-com选项。__

__使用\-cv和\-cf选项可以将平均速度和平均力作为温度因子输出到一个 \.pdb ↪ 614 文件，其中的坐标为  
平均坐标或\-ctime时刻的坐标。程序会对温度因子进行缩放，使其最大值为 10 。也可以使用\-scale  
选项更改缩放比例。要得到某一帧的速度或力，可以将\-b 和\-e选项都指定为所需帧的时间值。当对  
帧进行平均时，可能需要使用\-nojump选项来得到正确的平均坐标。如果选择了这些选项中的任何一  
个，程序会将每个原子的平均力和平均速度输出到一个 \.xvg ↪ 623 文件（由\-av或\-af选项指定）。__

__使用\-vd选项可以计算速度分布，即输出速度大小的分布。此外，文件中还会同时给出动能的分布。__

__关于如何输出选区的类似数据，请参阅 gmx trajectory ↪ 340 。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ox \[<\.xvg>\] coord\.xvg 可选 xvgr/xmgr文件__

__\-oxt \[<\.xtc/\.trr/\.\.\.>\] coord\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ，__

__tng ↪ 617__

__\-ov \[<\.xvg>\] veloc\.xvg 可选 xvgr/xmgr文件__

__\-of \[<\.xvg>\] force\.xvg 可选 xvgr/xmgr文件__

__\-ob \[<\.xvg>\] box\.xvg 可选 xvgr/xmgr文件__

__\-ot \[<\.xvg>\] temp\.xvg 可选 xvgr/xmgr文件__

__\-ekt \[<\.xvg>\] ektrans\.xvg 可选 xvgr/xmgr文件__

__\-ekr \[<\.xvg>\] ekrot\.xvg 可选 xvgr/xmgr文件__

__\-vd \[<\.xvg>\] veldist\.xvg 可选 xvgr/xmgr文件__

__\-cv \[<\.pdb>\] veloc\.pdb 可选 蛋白质数据库文件__

__\-cf \[<\.pdb>\] force\.pdb 可选 蛋白质数据库文件__

__\-av \[<\.xvg>\] all\_veloc\.xvg 可选 xvgr/xmgr文件__

__\-af \[<\.xvg>\] all\_force\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两__

__帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]com no 输出每组质心的数据__

__\-\[no\]pbc yes 根据质心使分子保持完整__

__\-\[no\]mol no 索引包含了分子编号而不是原子编号__

__\-\[no\]nojump no 移除越过盒子的原子跳跃__

__\-\[no\]x yes 输出X分量__

__\-\[no\]y yes 输出Y分量__

__\-\[no\]z yes 输出Z分量__

__\-ng <int> 1 要考虑的组的个数__

__\-\[no\]len no 输出向量长度__

__\-\[no\]fp no 全精度输出__

__\-bin <real> 1 速度直方图的分格宽度（单位：nm/ps）__

__\-ctime__

__<real> \-1 输出\-cv和\-cf时使用指定时刻帧的x，而不是平均的x__

__\-scale__

__<real>^0 \.pdb ↪^614 输出的缩放因子，^0 表示自动缩放__

#### 6\.4\.90 gmx trajectory

##### 概要

__gmx trajectory \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \]  
\[ \-n \[<\.ndx>\] \] \[ \-ox \[<\.xvg>\] \] \[ \-ov \[<\.xvg>\] \]  
\[ \-of \[<\.xvg>\] \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-tu \] \[ \-fgroup \] \[ \-xvg \]  
\[ \-\[no\]rmpbc \] \[ \-\[no\]pbc \] \[ \-sf \] \[ \-selrpos \]  
\[ \-seltype \] \[ \-select \] \[ \-\[no\]x \]  
\[ \-\[no\]y \] \[ \-\[no\]z \] \[ \-\[no\]len \]__

##### 说明

__gmx trajectory用于输出指定选区的坐标，速度和/或力。默认情况下，会输出所需向量的X，Y和Z  
分量，但指定一个或多个\-len，\-x，\-y和\-z会覆盖默认设置。__

__对于动态选区，目前会输出选区可能选中的所有位置的对应值。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc 可选__

__输入轨迹或单个构型： xtc ↪ 621 ， trr ↪ 619 ，__

__cpt ↪ 608 ， gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选__

__输入结构： tpr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 额外的索引组__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-ox \[<\.xvg>\] coord\.xvg 可选 每个位置的坐标与时间的函数__

__\-ov \[<\.xvg>\] veloc\.xvg 可选 每个位置的速度与时间的函数__

__\-of \[<\.xvg>\] force\.xvg 可选 每个位置的力与时间的函数__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0__

__读入轨迹第一帧的时间，即分析的起始时间（默认单位__

__ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的终止时间（默认单位__

__ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分__

__析时两帧之间的时间间隔（默认单位ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-fgroup__

__<selection>__

__轨迹文件中存储的原子（如果未设置，假定为前N个原__

__子）__

__\-xvg <enum> xmgrace 绘图格式：none，xmgrace，xmgr__

__\-\[no\]rmpbc yes 对每一帧的分子进行完整化__

__\-\[no\]pbc yes 计算距离时使用周期性边界条件__

__\-sf <file> 使用文件中提供的选区__

__\-selrpos <enum> atom__

__选区参考位置：atom，res\_com，res\_cog，mol\_com，__

__mol\_cog，whole\_res\_com，whole\_res\_cog，__

__whole\_mol\_com，whole\_mol\_cog，part\_res\_com，__

__part\_res\_cog，part\_mol\_com，part\_mol\_cog，__

__dyn\_res\_com，dyn\_res\_cog，dyn\_mol\_com，__

__dyn\_mol\_cog__

__\-seltype <enum> atom__

__默认选区输出位置：atom，res\_com，res\_cog，__

__mol\_com，mol\_cog，whole\_res\_com，__

__whole\_res\_cog，whole\_mol\_com，whole\_mol\_cog，__

__part\_res\_com，part\_res\_cog，part\_mol\_com，__

__part\_mol\_cog，dyn\_res\_com，dyn\_res\_cog，__

__dyn\_mol\_com，dyn\_mol\_cog__

__\-select__

__<selection> 要分析的选区__

__\-\[no\]x yes 输出X分量__

__\-\[no\]y yes 输出Y分量__

__\-\[no\]z yes 输出Z分量__

__\-\[no\]len no 输出向量长度__

#### 6\.4\.91 gmx trjcat

##### 概要

__gmx trjcat \[ \-f \[<\.xtc/\.trr/\.\.\.> \[\.\.\.\]\] \] \[ \-n \[<\.ndx>\] \] \[ \-demux \[<\.xvg>\] \]  
\[ \-o \[<\.xtc/\.trr/\.\.\.> \[\.\.\.\]\] \] \[ \-tu \] \[ \-xvg \]  
\[ \-b \] \[ \-e \] \[ \-dt \] \[ \-\[no\]settime \]  
\[ \-\[no\]sort \] \[ \-\[no\]keeplast \] \[ \-\[no\]overwrite \] \[ \-\[no\]cat \]__

##### 说明

__gmx trjcat用于按顺序将几个输入轨迹文件合并在一起。如果同一时刻的轨迹超过一帧，会使用后一  
文件中的那帧。可以使用\-settime选项指定每个文件的起始时间。输入文件来自命令行，这样你可以  
使用像gmx trjcat \-f \*\.trr \-o fixed\.trr 这样的技巧。使用\-cat选项可以将几个文件简单的粘  
贴在一起，而不会删除具有相同时间戳的帧。__

__如果指定的输出文件为输入文件中的一个，需要特别注意一点。在这种情况下，输出会追加到那个特定  
的输入文件，这样就不需要存储双倍的数据。显然，要追加的文件必须是起始时间最小的文件，因为输  
出只能追加到文件末尾。__

__如果指定\-demux选项，会读取N条轨迹，并将它们按照 \.xvg ↪ 623 文件中指定的顺序输出到另外一个文  
件中。此选项适用于副本交换动力学模拟。 \.xvg ↪ 623 文件的内容类似如下：__

__0 0 1 2 3 4 5  
2 1 0 2 3 5 4__

__第一个数字为时间，接下来的数字为轨迹编号。程序会收集与第一行数字对应的帧并输出到输出轨迹中。  
如果轨迹中的帧数与 \.xvg ↪ 623 文件中的不匹配，程序会自动决定如何处理。使用此选项时要小心。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.> \[\.\.\.\]\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-demux \[<\.xvg>\] remd\.xvg 可选 xvgr/xmgr文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xtc/\.trr/\.\.\.> \[\.\.\.\]\] trajout\.xtc__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

##### 控制选项

##### 选项 默认值 说明

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-b <time> \-1 读入第一帧的时间，即起始时间（单位：ps）__

__\-e <time> \-1 读入最后一帧的时间，即结束时间（单位：ps）__

__\-dt <time> 0__

__只输出时刻t除以dt的余数等于第一帧时间的帧，即两帧之__

__间的时间间隔（单位：ps）__

__\-\[no\]settime no 交互地设定每一输入文件在新输出文件中的起始时间__

__\-\[no\]sort yes 自动排序输入轨迹文件（而不是帧）__

__\-\[no\]keeplast no 将重叠帧输出到轨迹的末尾__

__\-\[no\]overwrite no 追加时覆盖重叠帧__

__\-\[no\]cat no 不删除重叠帧__

#### 6\.4\.92 gmx trjconv

##### 概要

__gmx trjconv \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-fr \[<\.ndx>\] \] \[ \-sub \[<\.ndx>\] \] \[ \-drop \[<\.xvg>\] \]  
\[ \-o \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-b \] \[ \-e \]  
\[ \-tu \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-skip \]  
\[ \-dt \] \[ \-\[no\]round \] \[ \-dump \] \[ \-t0 \]  
\[ \-timestep \] \[ \-pbc \] \[ \-ur \]  
\[ \-\[no\]center \] \[ \-boxcenter \] \[ \-box \]  
\[ \-trans \] \[ \-shift \] \[ \-fit \]  
\[ \-ndec \] \[ \-\[no\]vel \] \[ \-\[no\]force \] \[ \-trunc \]  
\[ \-exec \] \[ \-split \] \[ \-\[no\]sep \]  
\[ \-nzero \] \[ \-dropunder \] \[ \-dropover \]  
\[ \-\[no\]conect \]__

##### 说明

__gmx trjconv可使用多种方式转换轨迹文件：__

- __从一种格式转换到另一种格式__
- __选择一组原子的集合__
- __改变系统周期性的表示方式__
- __将多聚分子保持在一起__
- __将原子在盒子内居中__
- __将原子叠合到参考结构__
- __减少帧数__
- __更改每帧的时间戳（\-t0和\-timestep选项）__
- __选择某个量处于特定范围内的帧，这个量由 \.xvg ↪ 623 文件给出。__

__根据聚类分析所得的信息抽取子轨迹的\-sub 选项已经从gmx trjconv 中移除,成为\[gmx extract\-  
cluster\]功能的一部分\.__

__gmx trjcat ↪ 341 更适用于将多个轨迹文件合并起来。__

__程序支持以下输入和输出格式： \.xtc ↪ 621 ， \.trr ↪ 619 ， \.gro ↪ 610 ， \.g96 ↪ 609 , \.pdb ↪ 614 和 \.tng 。文件格式由文件扩  
展名决定。对 \.xtc ↪ 621 ， \.gro ↪ 610 和 \.pdb ↪ 614 输入格式， \.xtc ↪ 621 输出文件的精度取决于输入文件；对其他  
输入格式，输出文件的精度由\-ndec选项决定。如果指定了\-ndec选项，输出精度总是由此选项决定。__

__所有其他格式的精度都是固定的。 \.trr ↪ 619 输出文件可以是单精度或双精度，具体取决于 gmx trjconv  
二进制文件的精度。注意，只有 \.trr ↪ 619 ， \.tng , \.gro ↪ 610 和 \.g96 ↪ 609 格式的文件支持速度。__

__使用\-sep 选项可以将每一帧输出到单独的 \.gro ↪ 610 ， \.g96 ↪ 609 或 \.pdb ↪ 614 文件。默认情况下，所有帧都  
会输出到一个文件中。合并了所有帧的 \.pdb ↪ 614 文件可以使用rasmol \-nmrpdb 查看。__

__为节省磁盘空间，可以选择部分轨迹并将其输出到一个新的轨迹文件中。例如，可以去除蛋白质水溶液  
轨迹中的水分子。始终要保留原始的轨迹文件\!我们建议使用可移植的 \.xtc ↪ 621 格式进行分析，这样可以  
节省磁盘空间并得到可移植的文件。__

__在写入 \.tng 输出时，如果选区名称与分子名称一致，且所选原子与该分子的所有原子一致，则文件会包  
含数目正确的一个分子类型。否则，整个选区将被视为包含所有选原子的单一分子。__

__有两个选项可用于将轨迹叠合到参考结构，或者用于本性动力学分析等。第一个选项只是简单地叠合到  
结构文件中的参考结构。第二个选项是逐步叠合：第一时间帧叠合到结构文件中的参考结构，每个后续  
时间帧叠合到前一步的叠合结构。使用这种方法可以得到连续的轨迹，与使用常规叠合方法时得到的结  
果不同，例如，当蛋白质的构象转变很大时。__

__可以使用\-pbc选项指定周期性边界条件的处理方式：__

- __mol:将分子的质心至于盒子内，需要使用\-s 选项指定一个运行输入文件。__
- __res:将残基的质心置于盒子内。__
- __atom:将所有原子置于盒子内。__
- __nojump:检查原子是否穿过了盒子边缘，是的话将它们放回来。这样所有分子都可以保持完整（如  
果它们在初始构型中是完整的）。注意，这样可以确保轨迹连续，但分子可能扩散出盒子。如果提  
供了结构文件，此过程的初始构型取自结构文件，否则会使用第一帧的构型。__
- __cluster:将所选索引中的所有原子团簇化，使其到团簇质心的距离最近，团簇质心会进行迭代更  
新。注意，实际上只有存在一个团簇时，这种方法才能给出有意义的结果。幸运的是，处理之后可  
以使用轨迹查看器对此进行检查。另请注意，如果分子破碎了，这个选项也不会起作用。__
- __whole:只会将破碎的分子恢复完整。__

__对\-pbc的mol，res和atom选项，可以使用\-ur选项指定单位晶胞的表示方式。对于三斜盒子这  
三个选项会给出不同的结果，而对于长方盒子，给出的的结果相同。rect为普通的长方体形状。tric  
为三斜晶胞。compact将所有原子置于到盒子中心最近的位置。这有利于可视化，例如截角八面体或菱  
形十二面体。tric和compact选项所用的中心为tric（见下文），除非使用\-boxcenter选项指定  
了其他值。__

__可以使用 \-center选项将系统在盒子内居中。用户可以指定用于确定几何中心的组。对于 \-pbc和  
\-center选项，可以使用\-boxcenter 选项指定盒子中心的位置。可用的选项为：tric:盒向量总和  
的一半，rect:盒对角线的一半，zero:原点。如果需要居中并使所有分子都处于盒子内，可以使用  
\-center以及\-pbc mol选项。__

__可以使用\-box 选项指定新盒子的大小。此选项只适用于主要方向，因此通常只适用于长方盒子。如  
果只想修改某些方向，例如读取轨迹时，可以使用 \-1 将某一方向保持不变。如果只调用一次 gmx  
trjconv，将\-pbc，\-fit，\-ur和\-center选项组合起来并非总能达到目的。这种情况下可以考虑  
多次调用，同时参考GROMACS网站的一些建议。__

__使用\-dt选项可以减少输出中的帧数。这个选项依赖于输入轨迹中时间的准确性，因此如果它们不够准  
确，可以使用\-timestep选项来修改时间（可以同时进行）。为制作平滑的动画，可以利用 gmx filter ↪ 242  
程序，它可以在使用低通频率滤波的同时减少帧数，从而降低高频运动的走样。__

__如果指定了\-trunc 选项，gmx trjconv可以就地截断 \.trr ↪ 619 文件，即不会复制文件。当在磁盘I/O  
过程中运行崩溃时（即磁盘已满），或者合并两个连续的轨迹但不能有重复帧时，这个选项可能会用到。__

__使用\-dump 选项可以从轨迹文件中抽取处于或靠近指定时刻的轨迹帧，但这个选项只有当轨迹帧之间  
的时间间隔均匀时才能使用。如果轨迹中的帧不按时间顺序排列，结果不明确。__

__可以使用\-drop选项读取一个 \.xvg ↪ 623 文件中的时间和值。如果指定了\-dropunder和/或\-dropover  
选项，程序不会输出低于/高于相应指定值的轨迹帧。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选__

__结构\+质量（db）: tpr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

__\-fr \[<\.ndx>\] frames\.ndx 可选 索引文件__

__\-sub \[<\.ndx>\] cluster\.ndx 可选 索引文件__

__\-drop \[<\.xvg>\] drop\.xvg 可选 xvgr/xmgr文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xtc/\.trr/\.\.\.>\] trajout\.xtc__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ， tng ↪ 617__

__控制选项__

__选项 默认值 说明__

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0__

__读入轨迹最后一帧的时间，即分析的结束时间（默认单位__

__ps）__

__\-tu <enum> ps 时间的单位：fs，ps，ns，us，ms，s__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-skip <int> 1 每隔指定数目的帧输出一次，即输出帧的间隔__

__\-dt <time> 0__

__只输出时刻t除以dt的余数等于第一帧时间的帧，即两帧__

__之间的时间间隔（单位：ps）__

__\-\[no\]round no 将时间舍入到最接近的皮秒__

__\-dump <time> \-1 输出最接近指定时间的帧（单位：ps）__

__\-t0 <time> 0 起始时间（单位：ps）（默认：不更改）__

__\-timestep <time> 0 更改输入帧之间的时间步长（单位：ps）__

__\-pbc <enum> none PBC处理方式（完整说明见帮助文本）:none，mol，__

__res，atom，nojump，cluster，whole__

__\-ur <enum> rect 单位晶胞表示方式：rect，tric，compact__

__\-\[no\]center no 将原子在盒子内居中__

__\-boxcenter__

__<enum> tric \-pbc和\-center选项使用的中心：tric，rect，zero__

__\-box <vector> 0 0 0 新立方体盒子的大小（默认：来自输入文件）__

__\-trans <vector> 0 0 0 将所有坐标平移指定值。适用于与\-pbc mol \-ur compact__

__联合使用。__

__\-shift <vector> 0 0 0 所有坐标的偏移值为帧编号与指定值的乘积__

__\-fit <enum> none__

__将分子叠合到结构文件中的参考结构，可用选项：none，__

__rot\+trans，rotxy\+transxy，translation，transxy，__

__progressive__

__\-ndec <int> 3 \.xtc输出文件中小数的位数__

__\-\[no\]vel yes 如果可能，读取并输出速度__

__\-\[no\]force no 如果可能，读取并输出力__

__\-trunc <time> \-1 在指定时刻后截断输入轨迹文件（单位：ps）__

__\-exec <string> 对每个输出帧执行指定命令，帧编号作为命令的参数__

__\-split <time> 0 如果t除以指定值的余数等于第一帧的时间，打开新的输出__

__文件（单位：ps）__

__\-\[no\]sep no 将每一帧输出到单独的\.gro，\.g96或\.pdb文件__

__\-nzero <int> 0__

__如果指定了\-sep选项，文件名称编号的数字位数，会根据__

__需要补加 0__

__\-dropunder__

__<real>^0 舍弃低于指定值的所有帧__

__\-dropover \(^0\) 舍弃高于指定值的所有帧  
\-\[no\]conect no 输出 \.pdb ↪^614 文件时添加CONECT连接记录。有助于可视  
化非标准分子，如粗粒化的分子__

##### 补充说明

__gmx trjconv可能是最常用的后处理工具，用来处理坐标，处理周期性或者手动调整轨迹。利用它抽取  
特定的轨迹比较简单，但使用它处理轨迹的周期性时，一些选项不容易理解。下面对其中的一些进行说  
明。__

__\-pbc mol|res|atom指定以何种方式考虑PBC，是使分子的质心，残基的质心，还是每个原子处于盒  
子中。如果使用\-pbc atom所有原子都处于盒子之中，这样边界上的分子看起来破碎了。如果对破碎后  
的分子再使用一次\-pbc whole，将分子恢复完整，其效果与\-pbc mol类似。__

__\-pbc nojump可以保证分子的运动是连续的，就像体系处于真空中一样，分子连续地向各个方向扩散。  
在计算MSD这样的量的时候，需要这样考虑。但gmx msd在计算时已经考虑了这点，所以我们就无须  
先利用此选项对轨迹进行处理了。此选项对单个构型没有意义。__

__使用\-pbc mol|res|atom选项时，会使相应的中心处于盒子中，而盒子的显示方法则使用\-ur来控制。  
如果使用长方体盒子，\-ur的三种选项给出的结果相同，所以无需考虑此项。如果使用了三斜盒子，  
\-ur的三种选项给出的结果不同：\-ur tric粒子处于三斜盒子中，\-ur rect粒子处于长方盒子中，\-ur__

__compact粒子处于距盒子中心最近的位置，近似球形。__

__利用\-center选项可使某组原子在盒子内居中，运行时，会提示你选择要居中的组。此选项可以和\-pbc  
mol|res|atom一起使用，达到使某组原子居中，同时其他原子都处于盒子内的目的。__

__在使用\-ur tric|compact，\-pbc mol|res|atom|，\-center选项时，都需要定义盒子的中心。默认使  
用的盒子中心处于盒向量的一半处。但可以使用\-boxcenter改变：tric盒向量总和的一半，rect盒子  
对角线的一半，zero 0 。__

__上面的这几个选项可组合使用，但不能保证一定能满足需要，有时可能需要使用gmx trjconv多次。__

__注意，\-pbc和\-fit rot两个选项不能一起使用。否则程序运行错误，给出如下信息：__

__PBC condition treatment does not work together with rotational fit\.  
Please do the PBC condition treatment first and then run trjconv in a second step for␣  
↪the rotational fit\.  
First doing the rotational fit and then doing the PBC treatment gives incorrect␣  
↪results\!__

__这意味着凡同时涉及周期性和叠合的处理都需要分两次进行，而且必须先进行周期性处理，再进行叠合，  
否则结果错误。__

#### 6\.4\.93 gmx trjorder

##### 概要

__gmx trjorder \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-nshell \[<\.xvg>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-xvg \] \[ \-na \]  
\[ \-da \] \[ \-\[no\]com \] \[ \-r \] \[ \-\[no\]z \]__

##### 说明

__gmx trjorder可以根据到参考组原子的最小距离或z坐标（\-z 选项）对分子进行排序。使用距离排  
序时，需要指定一组参考原子和一组排序分子。对轨迹中的每一帧，所选分子会根据其编号为\-da的原  
子与参考组中所有原子之间的最小距离进行重新排序。如果\-da指定为 0 ，会使用分子的质心而不是  
原子。轨迹中的所有原子都会输出到输出轨迹。__

__对某些分析，可能会用到gmx trjorder。例如，分析距离蛋白质最近的n个水分子。在这种情况下，  
参考组为蛋白质，排序分子组为所有水分子的原子。当得到了前n个水分子的索引组后，排序后的轨迹  
用于任何GROMACS程序，以便分析最近的n个水分子。__

__如果输出为 \.pdb ↪ 614 文件，到参考目标的距离会存储在B因子字段中，以便使用诸如Rasmol之类的程  
序着色。__

__使用\-nshell选项可以输出参考组周围半径为 \-r的壳层内的分子数。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xtc/\.trr/\.\.\.>\] ordered\.xtc 可选__

__轨迹： xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，__

__pdb ↪ 614 ， tng ↪ 617__

__\-nshell \[<\.xvg>\] nshell\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧__

__之间的时间间隔（默认单位ps）__

__\-xvg__

__<enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-na \(^3\) 分子中的原子数  
\-da 1 计算距离时所用原子的编号， 0 表示使用质心  
\-\[no\]com no 使用到参考组质心的距离  
\-r 0 计算分子，如蛋白质，周围壳层内的分子数时，距离的截断值。  
\-\[no\]z no 根据z坐标排序分子__

#### 6\.4\.94 gmx tune\_pme

##### 概要

__gmx tune\_pme \[ \-s \[<\.tpr>\] \] \[ \-cpi \[<\.cpt>\] \] \[ \-table \[<\.xvg>\] \]  
\[ \-tablep \[<\.xvg>\] \] \[ \-tableb \[<\.xvg>\] \]  
\[ \-rerun \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-ei \[<\.edi>\] \] \[ \-p \[<\.out>\] \]  
\[ \-err \[<\.log>\] \] \[ \-so \[<\.tpr>\] \] \[ \-o \[<\.trr/\.cpt/\.\.\.>\] \]  
\[ \-x \[<\.xtc/\.tng>\] \] \[ \-cpo \[<\.cpt>\] \]  
\[ \-c \[<\.gro/\.g96/\.\.\.>\] \] \[ \-e \[<\.edr>\] \] \[ \-g \[<\.log>\] \]  
\[ \-dhdl \[<\.xvg>\] \] \[ \-field \[<\.xvg>\] \] \[ \-tpi \[<\.xvg>\] \]  
\[ \-tpid \[<\.xvg>\] \] \[ \-eo \[<\.xvg>\] \] \[ \-px \[<\.xvg>\] \]  
\[ \-pf \[<\.xvg>\] \] \[ \-ro \[<\.xvg>\] \] \[ \-ra \[<\.log>\] \]__

__\[ \-rs \[<\.log>\] \] \[ \-rt \[<\.log>\] \] \[ \-mtx \[<\.mtx>\] \]__

__\[ \-swap \[<\.xvg>\] \] \[ \-bo \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-bx \[<\.xtc>\] \]__

__\[ \-bcpo \[<\.cpt>\] \] \[ \-bc \[<\.gro/\.g96/\.\.\.>\] \] \[ \-be \[<\.edr>\] \]__

__\[ \-bg \[<\.log>\] \] \[ \-beo \[<\.xvg>\] \] \[ \-bdhdl \[<\.xvg>\] \]__

__\[ \-bfield \[<\.xvg>\] \] \[ \-btpi \[<\.xvg>\] \] \[ \-btpid \[<\.xvg>\] \]__

__\[ \-bdevout \[<\.xvg>\] \] \[ \-brunav \[<\.xvg>\] \] \[ \-bpx \[<\.xvg>\] \]__

__\[ \-bpf \[<\.xvg>\] \] \[ \-bro \[<\.xvg>\] \] \[ \-bra \[<\.log>\] \]__

__\[ \-brs \[<\.log>\] \] \[ \-brt \[<\.log>\] \] \[ \-bmtx \[<\.mtx>\] \]__

__\[ \-bdn \[<\.ndx>\] \] \[ \-bswap \[<\.xvg>\] \] \[ \-xvg <enum> \]__

__\[ \-mdrun <string> \] \[ \-np <int> \] \[ \-npstring <enum> \]__

__\[ \-ntmpi <int> \] \[ \-r <int> \] \[ \-max <real> \] \[ \-min <real> \]__

__\[ \-npme <enum> \] \[ \-fix <int> \] \[ \-rmax <real> \]__

__\[ \-rmin <real> \] \[ \-\[no\]scalevdw \] \[ \-ntpr <int> \]__

__\[ \-steps <int> \] \[ \-resetstep <int> \] \[ \-nsteps <int> \]__

__\[ \-\[no\]launch \] \[ \-\[no\]bench \] \[ \-\[no\]check \]__

__\[ \-gpu\_id <string> \] \[ \-\[no\]append \] \[ \-\[no\]cpnum \]__

__\[ \-deffnm <string> \]__

##### 说明

__对于给定数目 \-np或\-ntmpi 的总进程数，gmx tune\_pme可以系统地测试不同PME进程数对 gmx  
mdrun ↪ 276 运行时间的影响，并确定哪种设置最快。它还可以测试，能否通过将负载从Ewald求和的倒  
易空间部分转移到实空间部分来提高性能。测试时，只要将 \.tpr ↪ 619 文件， gmx mdrun ↪ 276 运行需要的选  
项一起传递给gmx tune\_pme即可。__

__gmx tune\_pme需要调用 gmx mdrun ↪ 276 ，因此需要使用\-mdrun 选项指定如何调用mdrun。取决于  
GROMACS的构建方式，可能需要诸如gmx mdrun，gmx\_d mdrun或gmx\_mpi mdrun之类的值。__

__可以使用MPIRUN 环境变量指定运行MPI程序的启动程序（默认为 mpirun）。注意，对某些MPI框  
架，可能需要提供机器或主机文件（hostfile）。这也可以通过MPIRUN变量来传递，例如__

__export MPIRUN="/usr/local/mpirun \-machinefile hosts"__

__注意，在这种情况下，通常需要编译和/或运行不带MPI支持的gmx tune\_pme，这样它才可以调用  
MPIRUN程序。__

__在进行实际的基准测试之前，如果指定了 \-check选项（默认），gmx tune\_pme会进行一个快速的检  
查，以确定 gmx mdrun ↪ 276 使用指定的并行设置是否能正常运行。请使用你要传递给 gmx mdrun ↪ 276 的  
常规选项调用gmx tune\_pme，并指定执行测试的进程数选项\-np，或线程数选项\-ntmpi。你也可以  
指定\-r选项对每个测试重复多次以得到更好的统计结果。__

__gmx tune\_pme可以测试各种实空间/倒空间的工作负载。可以使用\-ntpr选项控制额外输出的 \.tpr ↪ 619  
文件的数目，每个文件分别使用更大的截断距离和更小的傅里叶格点。通常，第一个测试（编号 0 ）使  
用输入 \.tpr ↪ 619 文件的设置；最后一个测试（编号ntpr）使用\-rmax 指定的库仑截断，同时使用略小  
的PME格点。在最后一个测试中，傅里叶间距会乘以rmax/rcoulomb。其余 \.tpr ↪ 619 文件使用的库仑  
半径（以及傅里叶间距）处于这两个极值之间，且间距相等。注意，如果只需要查找最佳的PME进程  
数，可以将\-ntpr选项指定为1;在这种情况下输入 \.tpr ↪ 619 文件将保持不变。__

__运行基准测试时，默认的 1000 个时间步对大多数MD系统来说应该足够了。动态负载均衡大约需要  
100 个时间步来适应局部的负载失衡，因此默认情况下， 100 步之后程序会重置时间步计数器。对于大  
型系统（>1M原子）以及更高精度的测量，应该将\-resetstep指定为更高的值。从 md\.log输出文__

##### 件中的DD负载失衡项，你可以知道多少步之后负载已经足够均衡了。示例命令：

__gmx tune\_pme \-np 64 \-s protein\.tpr \-launch__

__多次调用 gmx mdrun ↪ 276 之后，详细的性能信息会输出到perf\.out文件中。注意，在运行基准测试过  
程中，会产生一些临时文件（\-b\*选项），每个测试完成后程序会自动删除这些文件。__

__如果需要使用优化好的参数自动启动模拟，可以指定命令行选项\-launch。__

__程序对启用GPU的mdrun 提供了基本的支持。只要指定一个包含GPU ID号的字符串即可，这个字  
符串对应于运行优化时使用的\-gpu\_id命令行参数。这与mdrun \-gpu\_id完全相同，但没有映射，只  
是声明了符合条件的GPU设备。gmx tune\_pme会根据指定的GPU设备构造合适的mdrun调用命令。  
gmx tune\_pme不支持\-putasks。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-cpi \[<\.cpt>\] state\.cpt 可选 检查点文件__

__\-table \[<\.xvg>\] table\.xvg 可选 xvgr/xmgr文件__

__\-tablep \[<\.xvg>\] tablep\.xvg 可选 xvgr/xmgr文件__

__\-tableb \[<\.xvg>\] table\.xvg 可选 xvgr/xmgr文件__

__\-rerun \[<\.xtc/\.trr/\.\.\.>\] rerun\.xtc 可选__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-ei \[<\.edi>\] sam\.edi 可选 ED采样输入__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-p \[<\.out>\] perf\.out 通用输出文件__

__\-err \[<\.log>\] bencherr\.log 日志文件__

__\-so \[<\.tpr>\] tuned\.tpr 便携式xdr运行输入文件__

__\-o \[<\.trr/\.cpt/\.\.\.>\] traj\.trr 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，__

__tng ↪ 617__

__\-x \[<\.xtc/\.tng>\] traj\_comp\.xtc 可选 压缩轨迹（tng格式或便携xdr格__

__式）__

__\-cpo \[<\.cpt>\] state\.cpt 可选 检查点文件__

__\-c \[<\.gro/\.g96/\.\.\.>\] confout\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent，esp__

__\-e \[<\.edr>\] ener\.edr 能量文件__

__\-g \[<\.log>\] md\.log 日志文件__

__\-dhdl \[<\.xvg>\] dhdl\.xvg 可选 xvgr/xmgr文件__

__\-field \[<\.xvg>\] field\.xvg 可选 xvgr/xmgr文件__

__\-tpi \[<\.xvg>\] tpi\.xvg 可选 xvgr/xmgr文件__

__\-tpid \[<\.xvg>\] tpidist\.xvg 可选 xvgr/xmgr文件__

__\-eo \[<\.xvg>\] edsam\.xvg 可选 xvgr/xmgr文件__

__\-px \[<\.xvg>\] pullx\.xvg 可选 xvgr/xmgr文件__

__\-pf \[<\.xvg>\] pullf\.xvg 可选 xvgr/xmgr文件__

__\-ro \[<\.xvg>\] rotation\.xvg 可选 xvgr/xmgr文件__

__\-ra \[<\.log>\] rotangles\.log 可选 日志文件__

__\-rs \[<\.log>\] rotslabs\.log 可选 日志文件__

__\-rt \[<\.log>\] rottorque\.log 可选 日志文件__

__\-mtx \[<\.mtx>\] nm\.mtx 可选 Hessian矩阵__

__\-swap \[<\.xvg>\] swapions\.xvg 可选 xvgr/xmgr文件__

__\-bo \[<\.trr/\.cpt/\.\.\.>\] bench\.trr 全精度轨迹文件： trr ↪^619 ， cpt ↪^608 ，__

__tng ↪ 617__

__\-bx \[<\.xtc>\] bench\.xtc 压缩轨迹（便携式xdr格式）: xtc__

__\-bcpo \[<\.cpt>\] bench\.cpt 检查点文件__

__\-bc \[<\.gro/\.g96/\.\.\.>\] bench\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ，__

__pdb ↪ 614 ，brk，ent，esp__

__\-be \[<\.edr>\] bench\.edr 能量文件__

__\-bg \[<\.log>\] bench\.log 日志文件__

__\-beo \[<\.xvg>\] benchedo\.xvg 可选 xvgr/xmgr文件__

__\-bdhdl \[<\.xvg>\] benchdhdl\.xvg 可选 xvgr/xmgr文件__

__\-bfield \[<\.xvg>\] benchfld\.xvg 可选 xvgr/xmgr文件__

__\-btpi \[<\.xvg>\] benchtpi\.xvg 可选 xvgr/xmgr文件__

__\-btpid \[<\.xvg>\] benchtpid\.xvg 可选 xvgr/xmgr文件__

__\-bdevout \[<\.xvg>\] benchdev\.xvg 可选 xvgr/xmgr文件__

__\-brunav \[<\.xvg>\] benchrnav\.xvg 可选 xvgr/xmgr文件__

__\-bpx \[<\.xvg>\] benchpx\.xvg 可选 xvgr/xmgr文件__

__\-bpf \[<\.xvg>\] benchpf\.xvg 可选 xvgr/xmgr文件__

__\-bro \[<\.xvg>\] benchrot\.xvg 可选 xvgr/xmgr文件__

__\-bra \[<\.log>\] benchrota\.log 可选 日志文件__

__\-brs \[<\.log>\] benchrots\.log 可选 日志文件__

__\-brt \[<\.log>\] benchrott\.log 可选 日志文件__

__\-bmtx \[<\.mtx>\] benchn\.mtx 可选 Hessian矩阵__

__\-bdn \[<\.ndx>\] bench\.ndx 可选 索引文件__

__\-bswap \[<\.xvg>\] benchswp\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-mdrun <string> 用于运行模拟的命令，如gmx mdrun或gmx\_mpi mdrun__

__\-np <int> 1 运行测试的进程数（使用单独的PME进程时必须>2）__

__\-npstring <enum> np $MPIRUN选项的名称，用于指定要使用的进程数（np 或__

__n;如果不使用指定none）: np，n，none__

__\-ntmpi <int> 1 运行测试的MPI线程数（关闭MPI和mpirun）__

__\-r <int> 2 每个测试的重复次数__

__\-max <real> 0\.5 要测试的PME进程数的最大比例__

__\-min <real> 0\.25 要测试的PME进程数的最小比例__

__\-npme <enum> auto__

__处于\-min和\-max之间，对\-npme的所有可能值或合理__

__子集进行基准测试。auto会忽略\-min和\-max，根据\.tpr__

__文件中的npme推测一个值，并由此选择一个合理值：__

__auto，all，subset__

__\-fix <int> \-2__

__若指定值>=\-1，不改变PME进程的数目，而使用指定数,,,,,,,,__

__目的PME进程，测试时只改变rcoulomb和PME格点间__

__距。__

__\-rmax <real> 0__

__若指定值>0，用于\-ntpr>1的最大rcoulomb（增大__

__rcoulomb会导致傅里叶格点缩小）__

__\-rmin <real> 0 若指定值>0，用于\-ntpr>1的最小rcoulomb__

__\-\[no\]scalevdw yes 同时缩放rvdw与rcoulomb__

__\-ntpr <int> 0__

__进行基准测试的 \.tpr ↪ 619 文件的数目。根据\-rmin和\-rmax__

__创建具有不同rcoulomb缩放因子的文件，文件数目由指__

__定值确定。若<1，会自动选择要测试的 \.tpr ↪ 619 文件的数目__

__\-steps \(^1000\) 运行基准测试时，对指定的步数进行计时  
\-resetstep 1500 开始动态负载均衡计时前平衡指定的步数（在指定步数后重  
置循环计数器）  
\-nsteps \-1 如果指定值非负，在实际运行中执行指定的步数（覆  
盖 \.tpr ↪ 619 中的nsteps，增加 \.cpt ↪ 608 步数）  
\-\[no\]launch no 优化后启动实际模拟  
\-\[no\]bench yes 运行基准测试，还是仅仅创建输入 \.tpr ↪ 619 文件  
\-\[no\]check yes 运行基准测试前，检查mdrun是否可以并行  
\-gpu\_id 可以使用的GPU设备的唯一ID的列表  
\-\[no\]append yes 从检查点文件开始继续运行时，将输出追加到先前的输出文  
件中，而不是将模拟部分的编号添加到所有文件名中  
\-\[no\]cpnum no 保留检查点文件并对其名称进行编号（只用于\-launch）  
\-deffnm 设置默认的文件名称（只用于\-launch）__

##### 补充说明

##### 这个命令使用时实际有两个分支，按进程运行，按线程运行：

__\-np 8实际会变成mpirun \-np 8放到最前面，\-nmpi 8直接就是\-nmpi 8，然后才调节npme的数目__

__变化。虽然原理上明白了，但我尝试了依然只有gmx 2016的nmpi运行成功，np的任务，单独用mpirun都  
可以运行，gmx tune\_pme里面还是用不了。__

#### 6\.4\.95 gmx vanhove

##### 概要

__gmx vanhove \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-om \[<\.xpm>\] \] \[ \-or \[<\.xvg>\] \] \[ \-ot \[<\.xvg>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \]  
\[ \-sqrt \] \[ \-fm \] \[ \-rmax \] \[ \-rbin \]  
\[ \-mmax \] \[ \-nlevels \] \[ \-nr \] \[ \-fr \]  
\[ \-rt \] \[ \-ft \]__

##### 说明

__gmx vanhove用于计算Van Hove相关函数。Van Hove相关函数G\(r, t\)为 0 时刻位于r\_0的粒子在  
t时刻位于r\_0\+r位置处的概率。gmx vanhove计算G时不使用向量r，而使用r的长度。因此，它  
给出了粒子在时间t内移动距离r的概率。计算时会移除对周期性边界的跨越。还会校正因各向同性或  
各向异性压力耦合导致的缩放。__

__使用\-om选项可以输出整个矩阵与t和r的函数关系，或者与sqrt\(t\)和r的函数关系（\-sqrt选项）。__

__使用\-or选项可以输出一个或多个t值的Van Hove函数。可以使用\-nr选项指定时间数，\-fr选项  
指定时间之间的间隔。分格宽度可以使用\-rbin选项指定。程序会自动确定分格数目。__

__使用\-to选项可以输出函数到一定距离（\-rt选项指定）的积分与时间的函数关系。__

__对所有读入的帧，所选粒子的坐标都存储在内存中。因此程序可能会占用大量内存。使用 \-on和 \-to  
选项时程序可能会变得很慢。这是因为计算时间正比于帧数与\-fm或\-ft的乘积。注意，使用\-dt选  
项可以减少内存使用量和计算时间。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 结构\+质量（db）: tpr ↪^619 ， gro ↪^610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-om \[<\.xpm>\] vanhove\.xpm 可选 X PixMap兼容的矩阵文件__

__\-or \[<\.xvg>\] vanhove\_r\.xvg 可选 xvgr/xmgr文件__

__\-ot \[<\.xvg>\] vanhove\_t\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时__

__两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-sqrt <real> 0 矩阵轴使用sqrt\(t\)，其分格间距以sqrt\(ps\)为单位__

__\-fm <int> 0 矩阵中的帧数， 0 表示输出所有__

__\-rmax <real> 2 矩阵中r的最大值（单位：nm）__

__\-rbin <real> 0\.01 矩阵和\-or中的分格宽度（单位：nm）__

__\-mmax <real> 0 矩阵中的最大密度， 0 表示由计算值决定（单位：1/nm）__

__\-nlevels \(^81\) 矩阵的水平数  
\-nr 1 \-or输出文件中的曲线数  
\-fr 0 \-or输出文件中的帧间隔  
\-rt 0 \-ot输出文件的积分上限（单位：nm）  
\-ft \(^0\) \-ot输出文件中的帧数， 0 表示输出所有帧__

#### 6\.4\.96 gmx velacc

##### 概要

__gmx velacc \[ \-f \[<\.trr/\.cpt/\.\.\.>\] \] \[ \-s \[<\.tpr/\.gro/\.\.\.>\] \] \[ \-n \[<\.ndx>\] \]  
\[ \-o \[<\.xvg>\] \] \[ \-os \[<\.xvg>\] \] \[ \-b \] \[ \-e \]  
\[ \-dt \] \[ \-\[no\]w \] \[ \-xvg \] \[ \-\[no\]m \] \[ \-\[no\]recip \]  
\[ \-\[no\]mol \] \[ \-acflen \] \[ \-\[no\]normalize \] \[ \-P \]  
\[ \-fitfn \] \[ \-beginfit \] \[ \-endfit \]__

##### 说明

__gmx velacc用于计算速度自相关函数。使用\-m 选项可以计算动量自相关函数。__

__使用\-mol选项可以计算分子的速度自相关函数。在这种情况下，索引组应该由分子编号而不是原子编  
号组成。__

__使用\-os选项还可以得到（振动）功率谱的估计，它是速度自相关函数的傅里叶变换。请确保轨迹包  
含具有速度信息的帧（即原始的 \.mdp ↪ 612 文件中指定了 nstvout），并且数据采集点之间的时间间隔远  
远小于自相关函数的时间尺度。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.trr/\.cpt/\.\.\.>\] traj\.trr 全精度轨迹文件： trr ↪ 619 ， cpt ↪ 608 ， tng ↪ 617__

__\-s \[<\.tpr/\.gro/\.\.\.>\] topol\.tpr 可选__

__结构\+质量（db）: tpr ↪ 619 ， gro ↪ 610 ，__

__g96 ↪ 609 ， pdb ↪ 614 ，brk，ent__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] vac\.xvg xvgr/xmgr文件__

__\-os \[<\.xvg>\] spectrum\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0 只使用时刻t除以dt的余数等于第一帧时间的帧，即分析__

__时两帧之间的时间间隔（默认单位ps）__

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-\[no\]m no 计算动量自相关函数__

__\-\[no\]recip yes 谱图中X轴以cm^\-1为单位，而不是1/ps。__

__\-\[no\]mol no 计算分子的速度自相关函数__

__\-acflen <int> \-1 ACF的长度，默认为帧数的一半__

__\-\[no\]normalize yes 归一化ACF__

__\-P <enum> 0__

__用于ACF的Legendre多项式的阶数（ 0 表示不使用）:__

__0 ， 1 ， 2 ， 3__

__\-fitfn <enum> none__

__拟合函数类型：none，exp，aexp，exp\_exp，exp5，__

__exp7，exp9__

__\-beginfit \(^0\) 对相关函数进行指数拟合的起始时间  
\-endfit \-1 对相关函数进行指数拟合的终止时间，\-1表示直到结束__

#### 6\.4\.97 gmx view\(2019\)

##### 概要

__gmx view \[ \-f \[<\.xtc/\.trr/\.\.\.>\] \] \[ \-s \[<\.tpr>\] \] \[ \-n \[<\.ndx>\] \] \[ \-b \]  
\[ \-e \] \[ \-dt \]__

##### 说明

__gmx view是GROMACS的轨迹查看器。该程序可以读取轨迹文件，运行输入文件和索引文件，并在标  
准X Window屏幕上绘制分子的3D结构。此程序不需要高端图形工作站，甚至可以在单色屏幕上使用。__

__这个程序已经实现了以下功能：分子的3D显示，旋转，平移和缩放，原子标签，轨迹动画，PostScript  
格式的硬拷贝，在MIT\-X（real X）上运行时用户可以自定义原子过滤器，打开窗口和主题，用户友好  
的菜单，去除周期性的选项，显示计算盒子的选项。__

__还可以使用一些更常见的X命令行选项：\-bg，\-fg更改颜色，\-font fontname更改字体。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xtc/\.trr/\.\.\.>\] traj\.xtc__

__轨迹文件： xtc ↪ 621 ， trr ↪ 619 ， cpt ↪ 608 ，__

__gro ↪ 610 ， g96 ↪ 609 ， pdb ↪ 614 ， tng ↪ 617__

__\-s \[<\.tpr>\] topol\.tpr 便携式xdr运行输入文件__

__\-n \[<\.ndx>\] index\.ndx 可选 索引文件__

##### 控制选项

##### 选项 默认值 说明

__\-b <time> 0 读入轨迹第一帧的时间，即分析的起始时间（默认单位ps）__

__\-e <time> 0 读入轨迹最后一帧的时间，即分析的结束时间（默认单位ps）__

__\-dt <time> 0__

__只使用时刻t除以dt的余数等于第一帧时间的帧，即分析时两帧之__

__间的时间间隔（默认单位ps）__

##### 已知问题

- __Balls选项不可用__
- __有时会无缘无故地出现核心转储错误__

#### 6\.4\.97 gmx wham

##### 概要

__gmx wham \[ \-ix \[<\.dat>\] \] \[ \-if \[<\.dat>\] \] \[ \-it \[<\.dat>\] \] \[ \-is \[<\.dat>\] \]  
\[ \-iiact \[<\.dat>\] \] \[ \-tab \[<\.dat>\] \] \[ \-o \[<\.xvg>\] \]  
\[ \-hist \[<\.xvg>\] \] \[ \-oiact \[<\.xvg>\] \] \[ \-bsres \[<\.xvg>\] \]  
\[ \-bsprof \[<\.xvg>\] \] \[ \-xvg \] \[ \-min \] \[ \-max \]  
\[ \-\[no\]auto \] \[ \-bins \] \[ \-temp \] \[ \-tol \]  
\[ \-\[no\]v \] \[ \-b \] \[ \-e \] \[ \-dt \]  
\[ \-\[no\]histonly \] \[ \-\[no\]boundsonly \] \[ \-\[no\]log \] \[ \-unit \]  
\[ \-zprof0 \] \[ \-\[no\]cycl \] \[ \-\[no\]sym \] \[ \-\[no\]ac \]  
\[ \-acsig \] \[ \-ac\-trestart \] \[ \-nBootstrap \]  
\[ \-bs\-method \] \[ \-bs\-tau \] \[ \-bs\-seed \]  
\[ \-histbs\-block \] \[ \-\[no\]vbs \]__

##### 说明

__gmx wham是一个用于实现加权直方图分析方法（WHAM）的分析程序。它用于分析伞形采样模拟生成  
的输出文件，以计算平均力势（PMF）。__

__gmx wham目前尚未完全更新。它只支持第一个牵引坐标为伞形牵引坐标的牵引设置，如果需要分析多  
个坐标，所有的坐标都要使用相同的几何结构和维度。在大多数情况下，这不是个问题。__

__目前，程序支持三种输入模式。__

- __指定\-it选项，用户需要提供一个文件，其中包含伞形采样模拟的运行输入文件（ \.tpr ↪ 619 文件）  
的文件名称，此外，还要使用 \-ix选项提供另一个文件，其中包含mdrun 输出的 pullx文件  
的文件名称。 \.tpr ↪ 619 和pullx文件的顺序必须对应，即第一个 \.tpr ↪ 619 文件创建了第一个pullx  
文件，依此类推。__
- __与上一输入模式相同，但用户使用\-if选项提供牵引力输出文件的名称（pullf\.xvg）。程序会  
根据牵引力计算伞形势的位置。无法用于表格形式的伞形势能。__

__默认情况下，在WHAM中会使用在所有pullx/pullf文件中找到的所有牵引坐标。如果只想使用某些牵  
引坐标，可以提供一个牵引坐标选择文件（\-is选项）。选择文件必须为tpr\-files\.dat中的每个\.tpr  
文件提供一行说明。其内容必须包含\.tpr文件中每个牵引坐标对应的一个数字（ 0 或 1 ）。在这里， 1  
表示WHAM会使用此牵引坐标， 0 表示省略。示例：如果有三个\.tpr文件，每个文件包含 4 个牵引坐  
标，但只使用牵引坐标 1 和 2 ，那么coordsel\.dat文件的内容如下：__

__1100  
1100  
1100__

__默认情况下，输出文件为：__

__\-o PMF输出文件  
\-hist 直方图输出文件__

__注意，始终要检查直方图是否充分重叠。__

__程序假定伞形势为简谐势，力常数从 \.tpr ↪ 619 文件中读取。如果施加了非简谐的伞形力，可以使用\-tab  
提供一个表格形式的势能函数。__

##### WHAM 选项

- __\-bins:分析中使用的分格数__
- __\-temp:模拟温度__
- __\-tol:剖面（概率）变化小于指定容差时停止迭代__
- __\-auto:自动确定边界__
- __\-min, \-max:剖面的边界__

__可以使用\-b，\-e和\-dt选项限制用于计算剖面文件的数据点。需要调整 \-b选项以确保每个伞形窗  
口都达到了充分平衡。__

__如果指定了\-log选项（默认），程序会以能量单位输出势能剖面，否则会输出概率（\-nolog选项）。  
可以使用 \-unit选项指定单位。以能量单位输出时，第一个分格中的能量定义为零。如果需要将其他  
位置的自由能定义为零，可以使用\-zprof0选项（适用于自展法，见下文）。__

__对于环形或周期性的反应坐标（二面角，无渗透梯度的通道PMF），\-cycl选项很有帮助。gmx wham  
会利用系统的周期性生成一个周期性的PMF。程序假定反应坐标的第一个和最后一个分格是相邻的。__

__如果指定了\-sym选项，在输出之前会将势能剖面关于z=0对称化，这对于膜系统之类的体系可能有  
用。__

##### 并行

__如果可行，可以通过设置OMP\_NUM\_THREADS环境变量来控制gmx wham使用的OpenMP线程数。__

##### 自相关

__使用 \-ac 选项时，gmx wham 会估算每个伞形窗口的积分自相关时间（IACT）tau，并使用  
1/\[1\+2\*tau/dt\]作为相应窗口的权重。IACT会输出到 \-oiact 指定的文件中。在冗长输出模式下，  
所有自相关函数（ACF）都会输出到 hist\_autocorr\.xvg文件。由于在采样有限的情况下可能会严  
重低估IACT，用户可以指定\-acsig 选项（高斯函数的sigma，见iact\.xvg中的输出），使用高斯  
函数沿反应坐标对IACT进行平滑。注意，程序通过简单地积分ACF来估计IACT，且只考虑大于  
0\.05的ACF。如果要使用更复杂（但可能不太稳健）的方法，如双指数拟合，来计算IACT，可以使  
用 gmx analyze ↪ 183 计算IACT，并使用iact\-in\.dat文件（\-iiact选项）将其提供给gmx wham。在  
iact\-in\.dat文件中每个输入文件（pullx/f文件）对应一行，各输入文件中每个牵引坐标对应一列。__

##### 误差分析

##### 可以使用自展分析来估计统计误差。请小心使用，否则可能会大大低估统计误差。自展技术的更多背景

__和实例可以参考Hub, de Groot, Van der Spoel, JCTC\(2010\)6: 3713\-3720。\-Bootstrap选项用于定义  
自展的数目（如 100 ）。程序支持四种自展方法，可以使用\-bs\-method 选项选择。__

- __b\-hist:默认方法，将完整的直方图视为独立的数据点，通过为直方图赋予随机权重来进行自展  
（贝叶斯自展）。注意，沿反应坐标的每个点都必须被多个独立的直方图覆盖（例如 10 个直方图），  
否则会低估统计误差。__
- __hist: 将完整的直方图视为独立的数据点。对每个自展，从给定的N个直方图中随机选择N  
个直方图（允许重复，即放回采样）。为避免反应坐标上出现无数据的空隙，可以定义直方图块  
（\-histbs\-block选项）。在这种情况下，会将给定的直方图分成块，只有各块内部的直方图才会  
混合。注意，每块内的直方图必须能代表所有可能的直方图，否则会低估统计误差。__
- __traj: 根据给定的直方图生成新的随机轨迹，这样生成的数据点符从给定直方图的分布，并具  
有适当的自相关。每个窗口的自相关时间（ACT）必须是已知的，因此要指定\-ac选项或使用  
\-iiact 选项提供ACT。如果所有窗口的ACT都相同（并且已知），也可以使用\-bs\-tau选项  
指定它们。注意，在采样有限的情况下，即如果各个直方图在各自的位置不能代表完整的相空间，  
此方法可能会严重低估误差。__
- __traj\-gauss:与traj方法相同，但轨迹不是根据伞形直方图自展得到，而是来自均值和宽度都  
与伞形直方图相同的高斯函数。此方法得到的误差估计类似traj方法。__

__自展方法的输出：__

- __\-bsres:平均势能剖面和标准偏差__
- __\-bsprof:所有自展势能剖面文件__

__使用\-vbs选项（冗长自展）可以输出每个自展使用的直方图，并且使用traj自展方法时还会输出直  
方图的累积分布函数。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-ix \[<\.dat>\] pullx\-files\.dat 可选 通用数据文件__

__\-if \[<\.dat>\] pullf\-files\.dat 可选 通用数据文件__

__\-it \[<\.dat>\] tpr\-files\.dat 可选 通用数据文件__

__\-is \[<\.dat>\] coordsel\.dat 可选 通用数据文件__

__\-iiact__

__\[<\.dat>\] iact\-in\.dat 可选 通用数据文件__

__\-tab \[<\.dat>\] umb\-pot\.dat 可选 通用数据文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o \[<\.xvg>\] profile\.xvg xvgr/xmgr文件__

__\-hist \[<\.xvg>\] histo\.xvg xvgr/xmgr文件__

__\-oiact \[<\.xvg>\] iact\.xvg 可选 xvgr/xmgr文件__

__\-bsres \[<\.xvg>\] bsResult\.xvg 可选 xvgr/xmgr文件__

__\-bsprof \[<\.xvg>\] bsProfs\.xvg 可选 xvgr/xmgr文件__

##### 控制选项

##### 选项 默认值 说明

__\-xvg <enum> xmgrace xvg绘图格式：xmgrace，xmgr，none__

__\-min \(^0\) 势能剖面坐标的最小值  
\-max \(^0\) 势能剖面坐标的最大值  
\-\[no\]auto yes 自动确定最小值和最大值  
\-bins 200 势能剖面的分格数  
\-temp 298 温度  
\-tol 1e\-06 容差  
\-\[no\]v no 冗长模式  
\-b \(^50\) 分析的起始时间（单位：ps）  
\-e 1e\+20 分析的终止时间（单位：ps）  
\-dt 0 每dt ps分析一次  
\-\[no\]histonly no 输出直方图后退出  
\-\[no\]boundsonly no 确定最小值和最大值后退出（与\-auto联用）  
\-\[no\]log yes 输出前计算势能剖面的对数  
\-unit kJ 对数输出时能量的单位：kJ，kCal，kT  
\-zprof0 0 将指定位置处的势能剖面值定义为0\.0\(与\-log联用\)  
\-\[no\]cycl no 生成环形/周期性的势能剖面。假定最小值和最大值是同  
一点。  
\-\[no\]sym no 使势能剖面关于z=0对称  
\-\[no\]ac no 计算积分自相关时间并在wham中使用  
\-acsig 0 沿反应坐标，使用指定sigma值的高斯函数平滑自相关  
时间  
\-ac\-trestart  
^1__

__计算自相关函数时，每隔指定时间重新开始计算（单位：__

__ps）__

__\-nBootstrap <int> 0 自展的数目（如 200 ），用于估计统计不确定性__

__\-bs\-method <enum> b\-hist 自展方法：b\-hist，hist，traj，traj\-gauss__

__\-bs\-tau <real> 0__

__假定适用于所有直方图的自相关时间（ACT）。如果__

__ACT未知，使用\-ac选项。__

__\-bs\-seed <int> \-1 用于自展的随机种子。\(\-1表示使用时间\)__

__\-histbs\-block__

__<int>^8__

__混合直方图时，只混合\-histbs\-block指定块中的直方__

__图__

__\-\[no\]vbs no 冗长自展模式。输出每个自展的CDF和直方图文件。__

#### 6\.4\.98 gmx wheel

##### 概要

__gmx wheel \[ \-f \[<\.dat>\] \] \[ \-o \[<\.eps>\] \] \[ \-r0 \] \[ \-rot0 \]  
\[ \-T \] \[ \-\[no\]nn \]__

##### 说明

__gmx wheel用于绘制指定序列的螺旋轮示意图。输入序列来自 \.dat ↪ 608 文件，其中第一行为残基总数，  
接下来的每行包含一个残基名称。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f__

__\[<\.dat>\] nnnice\.dat 通用数据文件__

__输出文件选项__

__选项 默认文件 类型 说明__

__\-o__

__\[<\.eps>\] plot\.eps 封装的PostScript\(tm\)文件__

##### 控制选项

##### 选项 默认值 说明

__\-r0 <int> 1 序列中第一个残基的编号__

__\-rot0 <real> 0 旋转的初始角度（ 90 度即可）__

__\-T <string> 旋轮中心的文字（必须少于 10 个字符，否则会覆盖旋轮）__

__\-\[no\]nn yes 是否显示编号__

#### 6\.4\.99 gmx x2top

##### 概要

__gmx x2top \[ \-f \[<\.gro/\.g96/\.\.\.>\] \] \[ \-o \[<\.top>\] \] \[ \-r \[<\.rtp>\] \]  
\[ \-ff \] \[ \-\[no\]v \] \[ \-nexcl \] \[ \-\[no\]H14 \]  
\[ \-\[no\]alldih \] \[ \-\[no\]remdih \] \[ \-\[no\]pairs \] \[ \-name \]  
\[ \-\[no\]pbc \] \[ \-\[no\]pdbq \] \[ \-\[no\]param \] \[ \-\[no\]round \]  
\[ \-kb \] \[ \-kt \] \[ \-kp \]__

##### 说明

__gmx x2top可以根据坐标文件生成拓扑文件的原型。当根据原子名称和成键数目定义原子的杂化状态  
时，程序会假定结构中包含所有的氢原子。此程序还可以创建一个 \.rtp ↪ 615 条目，你可以将它添加到力场  
目录下的 \.rtp ↪ 615 数据库中。__

__如果指定了\-param选项，会将所有相互作用的平衡距离，键角和力常数写入拓扑中的相应位置。平衡  
距离和键角来自输入坐标，力常数由命令行选项指定。目前程序支持的力场为：__

__G53a5: GROMOS96 53a5力场（官方发布）__

__oplsaa OPLS\-AA/L全原子力场（ 2001 氨基酸二面体）__

__使用此程序时需要一个相应的atomname2type\.n2t数据文件，它位于力场库目录中。有关文件格式的  
详细信息，请查阅参考手册第 5 章↪ 524 。默认情况下，可以交互地选择力场，但也可以使用\-ff选项在  
命令行中指定上述力场的简短名称。在这种情况下，gmx x2top会到指定的力场目录下查找相应的文  
件。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.gro/\.g96/\.\.\.>\] conf\.gro 结构文件： gro ↪^610 ， g96 ↪^609 ， pdb ↪^614 ，brk，__

__ent，esp tpr ↪ 619__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-o__

__\[<\.top>\] out\.top 可选 拓扑文件__

__\-r__

__\[<\.rtp>\] out\.rtp 可选 pdb2gmx使用的残基类型文件__

##### 控制选项

##### 选项 默认值 说明

__\-ff <string> oplsaa 模拟使用的力场类型。select 表示交互式地进行选择。__

__\-\[no\]v no 在\.top文件中输出详细的生成信息。__

__\-nexcl \(^3\) 相互作用的排除数  
\-\[no\]H14 yes 对氢原子使用第三近邻相互作用  
\-\[no\]alldih no 生成所有的正常二面角  
\-\[no\]remdih no 移除同一键上的反常二面角  
\-\[no\]pairs yes 在拓扑文件中输出1\-4相互作用（原子对）  
\-name ICE 指定分子名称  
\-\[no\]pbc yes 使用周期性边界条件。  
\-\[no\]pdbq no 使用 \.pdb ↪ 614 文件提供的B因子作为原子电荷__

__\-\[no\]param yes 将参数输出中到拓扑中__

__\-\[no\]round yes 对测量值进行舍入__

__\-kb <real> 400000 键的力常数（单位：kJ/mol/nm^2）__

__\-kt <real> 400 键角的力常数（单位：kJ/mol/rad^2）__

__\-kp <real> 5 二面角的力常数（单位：kJ/mol/rad^2）__

##### 已知问题

##### • 原子类型的选择方法很粗糙。没有使用化学信息

##### • 周期性边界条件会导致成键信息错误

##### • 不会生成反常二面角

- __原子到原子类型的转换表（数据目录中的atomname2type\.n2t文件）不完整。请扩展此文件并将  
结果发送给GROMACS团队人员。__

##### 补充说明

__理论上只要能在对应的力场中找到构型中的各个原子类型，那么gmx x2top可以支持所有GROMACS  
的力场。当然输出的拓扑文件原型需要进行很多修改，因此使用此工具需要对拓扑文件足够熟悉。__

#### 6\.4\.100 gmx xpm2ps

##### 概要

__gmx xpm2ps \[ \-f \[<\.xpm>\] \] \[ \-f2 \[<\.xpm>\] \] \[ \-di \[<\.m2p>\] \] \[ \-do \[<\.m2p>\] \]  
\[ \-o \[<\.eps>\] \] \[ \-xpm \[<\.xpm>\] \] \[ \-\[no\]w \] \[ \-\[no\]frame \]  
\[ \-title \] \[ \-\[no\]yonce \] \[ \-legend \]  
\[ \-diag \] \[ \-size \] \[ \-bx \] \[ \-by \]  
\[ \-rainbow \] \[ \-gradient \] \[ \-skip \]  
\[ \-\[no\]zeroline \] \[ \-legoffset \] \[ \-combine \]  
\[ \-cmin \] \[ \-cmax \]__

##### 说明

__gmx xpm2ps可以将XPixelMap矩阵文件转换为漂亮的颜色映射图。如果提供了正确的矩阵格式，也  
可以显示标签和坐标轴。矩阵数据可以由其他程序生成，如 2019 版的 gmx do\_dssp ↪ 225 ， gmx rms ↪ 309  
或 gmx mdmat ↪ 275 。__

__可以选择性地使用\-di选项指定一个\.m2p文件，其中包含了设定的参数。对大多数参数提供了合理  
的默认值。 y 轴的默认设置与 x 轴相同。字体名称的默认等级为：标题\->图例；标题\->（x轴\-> y  
轴\-> y刻度）\-> x刻度，例如，设置标题字体相当于设置了所有字体，设置x轴字体相当于设置y轴  
字体，设置y刻度字体相当于设置了x刻度字体。__

__如果没有提供\.m2p 文件，程序会根据命令行选项指定多数设置。其中最重要的选项是\-size，它以  
postscript单位指定了整个矩阵的大小。此选项也可以使用\-bx和\-by选项（以及\.m2p文件中的相__

##### 6\.4\. 命令说明 363

##### 应参数）覆盖，它们指定了单个矩阵元素的大小。

__使用 \-f2选项可以提供第二个矩阵文件。程序会同时读取两个矩阵文件，并绘制第一个矩阵（\-f选  
项）的左上半部分以及第二个矩阵（\-f2选项）的右下半部分。对角线部分的值来自\-diag选项指定  
的矩阵文件。将\-diag 选项指定为none，可以不绘制对角线部分。在这种情况下，会生成一个新的颜  
色映射图，其中红色渐变表示负值，蓝色渐变表示正值。如果两个矩阵的颜色编码和图例标签完全相同，  
那么只会显示一个图例，否则会显示两个单独的图例。可以使用\-combine选项选择其他操作对矩阵进  
行组合。输出值的范围会自动设置为组合矩阵的实际范围。也可以用\-cmin和\-cmax选项覆盖。__

__可以将\-title 选项指定为none以忽略标题，或指定为ylabel 以便在Y轴标签位置显示标题（平  
行于 y 轴）。__

__可以使用\-rainbow选项将暗淡的灰度矩阵转换为更吸引人的彩色图片。__

__使用\-xpm选项可以将合并或彩虹矩阵输出到XPixelMap文件。__

##### 选项

##### 输入文件选项

##### 选项 默认文件 类型 说明

__\-f \[<\.xpm>\] root\.xpm X PixMap兼容的矩阵文件__

__\-f2 \[<\.xpm>\] root2\.xpm 可选 X PixMap兼容的矩阵文件__

__\-di \[<\.m2p>\] ps\.m2p 可选，库 mat2ps的输入文件__

##### 输出文件选项

##### 选项 默认文件 类型 说明

__\-do \[<\.m2p>\] out\.m2p 可选 mat2ps的输入文件__

__\-o \[<\.eps>\] plot\.eps 可选 封装的PostScript\(tm\)文件__

__\-xpm__

__\[<\.xpm>\] root\.xpm 可选 X PixMap兼容的矩阵文件__

##### 控制选项

##### 选项 默认值 说明

__\-\[no\]w no 查看输出的 \.xvg ↪ 623 ， \.xpm ↪ 620 ， \.eps ↪ 609 和 \.pdb ↪ 614 文件__

__\-\[no\]frame yes 显示图框，刻度，标签，标题和图例__

__\-title <enum> top 显示标题的位置：top，once，ylabel，none__

__\-\[no\]yonce no 只显示一次Y轴标签__

__\-legend <enum> both 显示图例：both，first，second，none__

__\-diag <enum> first 对角元素来源：first，second，none__

__\-size <real> 400 矩阵的水平尺寸，ps单位__

__\-bx <real> 0__

__元素x的大小，覆盖\-size 选项（若未指定\-by还会__

__覆盖y的大小）__

__\-by <real> 0 元素y的大小__

__\-rainbow <enum> no 彩虹颜色，将白色转换为何种颜色：no，blue，red__

__\-gradient <vector> 0 0 0 将颜色映射重新缩放为从白色\{1,1,1\}到\{r,g,b\}的平滑__

__渐变__

__\-skip <int> 1 每隔指定行列输出一次__

__\-\[no\]zeroline no 在 \.xpm ↪ 620 矩阵中坐标轴标签为零的位置插入一条线__

__\-legoffset <int> 0 忽略 \.xpm ↪ 620 文件的前N种颜色对应的图例__

__\-combine <enum> halves 组合两个矩阵的方法：halves，add，sub，mult，div__

__\-cmin \(^0\) 组合输出的最小值  
\-cmax \(^0\) 组合输出的最大值__

### 6\.5 不同版本之间的命令更改

##### 自GROMACS 5\.0开始，一些分析命令（以及其他一些命令）发生了重大变化。

##### 其中的一个主要驱动因素是，下面提到的许多新工具现在都可以通过一个或多个命令行选项接受选区，

##### 而不是仅仅提示输入静态索引组。为了充分利用选区，命令的接口有所改变，不再支持以前的一些命令

##### 行选项，因为使用适当的选区可以达到相同的效果。有关如何使用选区的其他信息，请参阅选区语法和

##### 用法↪ 371 。

##### 在此过程中，我们移除了一些旧的分析命令，以便通过替代工具提供更强大的功能。对于那些已经移除

##### 或替换的命令，此页面介绍如何使用新工具执行相同的任务。对于新命令，这里给出有关可用功能的简

##### 要说明。完整说明请参阅新命令的帮助链接。

##### 本节仅列出重大变化；添加/移除选项或修复错误等小修改通常不包括在内。

##### 有关功能更改的更多信息，请查看发布说明↪ 381 。

#### 2020 版

____gmx convert\-trj____

##### 新

__引入了 gmx convert\-trj ↪ __??__ ，支持选区语法,用于改变轨迹文件的格式（以前使用 gmx trjconv ↪ __??__ 完成,但  
不支持选区语法）。__

____gmx extract\-cluster____

__新__

__引入了 gmx extract\-cluster ↪ __??__ ，支持选区语法,__

__用于根据聚类分析的输出结果来写出部分轨迹。__

__gmx trjconv ↪ __??__ 中的相应选项\-sub已移除。__

#### 2018 版

____gmx trajectory____

##### 新

__gmx trajectory ↪ 340 支持选区，可视为 gmx traj ↪ 337 的改进版。它支持输出根据选区计算出的位置的坐标，  
速度和/或力。__

#### 2016 版

##### 对原子的任意一部分子集进行分析

##### 对那些在新的分析框架中实现的工具，即便轨迹中只含有输入结构文件中原子的一部分，现在可以使用。

____gmx insert\-molecules____

##### 改进

__gmx insert\-molecules ↪ 264 增加了一个选项\-replace，这样可以将分子插入到已溶剂化的构型中，并替  
换任何重叠的溶剂原子。在完全溶剂化的盒子中，也可以只选择溶剂原子的一部分子集，这样可以将  
分子插入到溶剂的某个区域中（\-replace支持选区，也可以使用not within 1 of \.\.\. 这样的表达  
式）。__

____gmx rdf____

##### 改进

##### 输出RDF的归一化方法可以是径向数密度。

____gmx genconf____

__简化__

__移除了\-block，\-sort和\-shuffle选项。__

#### 5\.1 版

##### 通用

__自5\.0起不再支持符号链接。调用命令的唯一方法是 gmx 。__

##### 6\.5\. 不同版本之间的命令更改 367

____gmx pairdist____

__新__

__引入支持选区的 gmx pairdist ↪ 295 ，以替代 gmx mindist ↪ 280 （gmx mindist仍然可以使用，且保持不变）。  
它可以计算一对选区之间的最小/最大成对距离，每个残基的最小距离或从单个点到一组残基质心的距  
离。__

____gmx rdf____

##### 重写

__5\.1版本的 gmx rdf ↪ 307 已重写，以支持使用选区来指定要计算RDF的点。除了可以使用新的命令行选  
项来指定选区之外，接口大致相同。此外，还进行了以下额外更改：__

- __移除了\-com和\-rdf选项。可以使用选区达到同样的目的：  
__\-__ \-com可以替换为使用com of 作为参考选区。  
__\-__ \-rdf可以替换为一组合适的选区（例如res\_com of ），也可以使用\-seltype  
代替。__
- __增加了\-rmax选项，用于指定RDF的截断距离。如果其指定值明显小于盒子大小的一半，当可  
以使用基于格点的邻区搜索时，可以显著加快计算速度。__
- __移除了\-hq和\-fade 选项，因为它们只是简单地对原始数据进行后处理，这些步骤可以在分析  
完成后轻松进行。__

#### 5\.0 版

##### 通用

__5\.0版引入了 __gmx__ 封装二进制文件。为了向后兼容，此版本默认会为旧工具创建符号链接：例如，  
g\_order 等价于gmx order ，而g\_order只是文件系统上的一个符号链接。__

____g\_bond____

##### 替代

__此工具已在5\.0中移除。替代工具为 gmx distance ↪ 220 。__

__可以将现有索引文件提供给 gmx distance ↪ 220 ，它会计算相同的距离。不同之处在于：__

- __\-blen和\-tol选项的默认值不同。__
- __可以使用\-binw控制输出直方图。__
- __不支持\-aver和\-averdist选项。但是，可以使用\-oav（对应使用\-averdist的\-d选项），  
\-oall（对应不使用\-averdist的\-d选项），\-oh（对应使用\-aver的\-o 选项），\-allstat  
（对应不使用\-aver的\-l 选项）来指定计算哪些项。__

__你可以生成任何输出文件的组合。与g\_bond相比，gmx distance \-oall目前缺少输出列标签的功能。__

____g\_dist____

__替代__

__此工具已在5\.0中移除。代替工具为 gmx distance ↪ 220 （对于大多数选项）或 gmx select ↪ 322 （对于\-dist  
或\-lt）。__

__如果你使用g\_dist计算距离时指定了index\.ndx中的索引组A和B，那么下面的gmx distance命  
令可以计算相同的距离：__

__gmx distance\-n index\.ndx\-select'com of group"A"plus com of group"B"'\-oxyz\-oall__

__\-nopbc选项替代了\-intra选项。__

__对于\-dist D，可以将其替换为下面的gmx select选项进行相同的计算：__

__gmx select\-n index\.ndx\-select'group"B"and within D of com of group"A"'\-on/\-oi/\-os/\-olt__

__你可以选择最适合自己后处理需要的输出选项（\-olt取代了g\_dist \-dist \-lt）__

____gmx distance____

##### 新

__引入支持选区的 gmx distance ↪ 220 ，用于替代那些计算固定原子对（或组的质心）之间的距离的各种工具。  
它结合了g\_bond和g\_dist的特性，可以计算原子对或组质心之间的一个或多个距离，并提供了其中  
一个工具可用的输出选项的组合。__

____gmx gangle____

##### 新

__引入支持选区的 gmx gangle ↪ 245 以替代g\_sgangle。除支持原子\-原子向量之外，质心也可以作为向量的  
端点，而且还可以计算一些额外的角度类型。此命令还基本支持计算三个原子和/或质心之间的法向角  
度，这样它也可以替代 gmx angle ↪ 186 的部分功能。__

____gmx protonate____

##### 替代

##### 这是一个非常古老的工具，最初是为联合原子力场编写的，在运行轨迹之后，必须使用此工具添加所有

__的氢原子，以便计算诸如距离限制违反之类的量。要简单地对结构进行质子化可以使用 gmx pdb2gmx ↪ 297 。  
如果还有很大的兴趣，我们可能会在将来转向新的拓扑格式后重新引入它。__

____gmx freevolume____

__新__

__在5\.0版本中引入此工具。它使用蒙特卡洛采样方法计算盒子内的自由体积的分数（使用给定大小的探  
针）。__

____g\_sas____

##### 重写

__在5\.0版本中重写了此工具，并重新命名为 gmx sasa ↪ 320 （底层的表面积计算算法仍然相同）。__

__新工具的主要区别在于支持选区。可以使用\-surface选项指定要计算的（可能是动态的）选区，而不  
需要根据提示输入索引组。可以使用\-output选项指定任意数目的输出组，这样可以在一次运行中计  
算表面积的多个部分。现在始终会计算\-surface组的总表面积。__

__此工具不再自动将表面划分为疏水区域和亲水区域，并且不再支持 \-f\_index 选项。可以通过为  
\-output指定合适的选区得到相同的结果。如果想得到与旧工具计算组A输出组B相同的结果可以使  
用下面的命令：__

__gmx sasa\-surface'group"A"'\-output'"Hydrophobic"group"A"and charge\{\-0\.2 to 0\.2\};  
↪"Hydrophilic"group"B"and not charge\{\-0\.2 to 0\.2\};"Total"group"B"'__

__现在，只有单独指定\-odg选项时才会计算溶剂化自由能的估计值，并会将其写入单独的文件中。__

__当前的新工具未实现用于位置约束文件的输出选项\-i，但如果需要也很容易添加。__

____g\_sgangle____

##### 替代

__此工具已在5\.0中移除。可以使用 gmx gangle ↪ 245 （用于计算角度）和 gmx distance ↪ 220 （用于\-od，\-od1，  
\-od2）替代。__

__如果在运行g\_sgangle时指定了index\.ndx中的索引组A和B，那么可以使用下面的gmx gangle的  
命令计算相同的角度：__

__gmx gangle\-n index\.ndx\-g1 vector/plane\-group1'group"A"'\-g2 vector/plane\-group2'group"B  
↪"'\-oav__

__你需要为\-g1和\-g2选项选择vector或plane，具体取决于你指定的索引组。__

__如果index\.ndx中只有一个索引组A，并使用g\_sgangle \-z 或\-one，你可以使用：__

__gmx gangle\-n index\.ndx\-g1 vector/plane\-group1'group"A"'\-g2 z/t0 \-oav__

__对于距离，你可以根据需要使用 gmx distance ↪ 220 计算一个或多个距离。使用新的选区语法，支持计算组  
的中心或单个原子之间的距离。__

____genbox____

__此工具已拆分为 gmx solvate ↪ 328 和 gmx insert\-molecules ↪ 264 两个工具。__

____tpbconv____

__此工具已重新命名为 gmx convert\-tpr ↪ 203 。__

### 6\.6 专题

__这些专题的信息也可以在命令行中使用gmx help topic 获取。__

#### 选区语法和用法

##### 选区语法和用法

##### 选区用于选择原子/分子/残基以进行后续分析。与传统的索引文件不同，选区可以是动态的，即，对轨

##### 迹中的不同帧选择不同的原子。GROMACS手册的“分析”一节中对选区作了简短的介绍，并给出了一

##### 些建议。当你初次接触选区概念时，这些建议可以帮助你熟悉它。下面将就选区的技术细节和语法方面

##### 给出更加详细的说明。

##### 不同分析工具需要的选区数目也不相同，对选区的解读也不一样，但大致意思仍然相同：每个选区最终

__都归结为一套位置（a set of position），位置可以是一些原子的原子位置，质心，或几何中心。分析工具  
可使用这些位置进行分析，这样处理时更加灵活。需要注意的是，某些分析工具对允许使用的选区种类  
可能存在限制。__

##### 在命令行中指定选区

##### 如果没有在命令行中提供选区，分析工具会提示你交互式地输入选区（对大多数工具而言，在这种情况

##### 下也可以用管道提供选区）。尽管测试时这样做很方便，但当选区很复杂，或将其用于脚本时，在命令行

##### 中提供选区更为容易。

##### 每个工具用于指定选区的命令行参数都不一样（参见每个工具的帮助文档）。你可以传递包含所有选区

##### 的单个字符串（以分号分隔），也可以传递多个字符串，每个字符串包含一个选区。注意，你需要将选区

__用引号引起来，以防止shell对它们进行转换。__

__如果你设置了一个选区命令行参数，但没有提供任何选区，分析工具会提示你交互式地为该参数输入选  
区。如果选区命令行参数是可选的，这一作法很有用，因为在这种情况下工具通常不会给出输入提示。__

__要使用一个文件提供选区，可在与选区参数对应的选区位置使用\-sf file\.dat（例如 \-select \-sf  
file\.dat）。通常情况下，\-sf参数从提供的文件中读取选区，并将它们赋值给所有已设置但尚未指定  
选区的选区参数。有一种特殊情况是，单独指定\-sf而没有前置的选区参数，这时程序会把\-sf指定  
的选区赋值给所有（尚未设置）的必需选区参数（即那些如果命令行没有提供选区，就会给出交互式提  
示的选区参数）。__

__要使用传统索引文件中的组（group），可以使用参数 \-n提供一个文件。组的使用方法可参见《语法》  
小节。如果没有提供此选项，就会生成默认组。默认组的生成逻辑与非选区工具的相同。__

##### 根据分析工具的不同，可能会有两个额外的命令行参数供使用，以控制分析工具行为：

- __\-seltype用于指定对每个选区要计算的默认位置类型。__
- __\-selrpos用于指定按坐标选择原子时使用的默认位置类型。__

__关于这些选项的更多信息，参见《位置》小节。__

__支持选区的工具会将选区应用于结构/拓扑和/或轨迹文件。如果分析工具将选区同时用于二者（通常由  
\-s指定结构/拓扑，\-f指定轨迹），那么轨迹文件只用于获取坐标信息，所有其他信息，如原子名称和  
残基信息，都来自结构/拓扑文件中。如果分析工具只使用结构文件，或者只提供了结构文件对应的输  
入参数，那么坐标也来自结构文件。例如，要使用分析工具从\.pdb/\.gro文件中选择原子，同时为工  
具提供了两个选项，请（只）使用\-s 选项指定文件。如果轨迹文件与结构文件不一致，例如各自的原  
子名称不同，程序不会给出警告。因为程序只会检查原子数目。许多支持选区的工具还提供了\-fgroup  
选项，用于指定轨迹中出现的原子索引，以处理轨迹仅包含拓扑/结构文件中的原子的一部分的情况。__

##### 选区语法

##### 一套选区由一个或多个选区组成，彼此以分号分隔。每个选区定义了一套位置用于分析。每个选区也可

##### 以用一个前置字符串进行命名，以便在某些环境，如图例中使用其名称。如果未提供名称，则会自动以

##### 描述选区的字符串作为名称。

##### 在交互式输入中，语法稍有不同：换行符也可用以分隔选区。如果需要，可使用\\后接换行符来续行。

##### 注意，上述作法只适用于真正的交互式输入，而不适用于通过其他渠道，比如管道，提供选区的情况。

##### 可以使用变量存储选区表达式。定义变量的语法如下：

__VARNAME=EXPR ;__

__其中EXPR可以是任何合法的选区表达式。定义后，在任何EXPR合法的地方都可以使用VARNAME。__

__选区包含三种主要的表达式类型：定义原子的表达式（ATOM\_EXPR），定义位置的表达式（POS\_EXPR），  
以及归结为数值的（NUM\_EXPR）表达式。每个选区应是一个POS\_EXPR或一个ATOM\_EXPR（后者会自  
动转换为位置）。基本规则如下：__

__类似于NUM\_EXPR1 < NUM\_EXPR2这样的表达式会求值为一个 ATOM\_EXPR，其中包含所有使比较  
表达式成立的原子。__

__原子表达式可以与逻辑操作结合使用，比如 not ATOM\_EXPR, ATOM\_EXPR and ATOM\_EXPR，或  
ATOM\_EXPR or ATOM\_EXPR。括号可用于改变求值顺序。__

__ATOM\_EXPR表达式能够以各种方式转换为POS\_EXPR表达式，详见《位置》小节。__

__POS\_EXPR表达式可转换为NUM\_EXPR表达式，其语法类似于x of POS\_EXPR。目前仅支持单个  
位置，比如表达式x of cog of ATOM\_EXPR。__

__某些关键词基于字符串的值，比如原子名称，来选中原子。对这些关键词，可以使用通配符（如name  
"C"）或正则表达式（如resname "R\[AB\]"）。程序会自动根据字符串猜测匹配类型：如果字符串包含  
除字母，数字，或 ?以外的字符，就被视为一个正则表达式。要强制使用字符串的字面内容进行匹  
配，可以使用name = "C"来匹配字面意义的C。要强制使用其他匹配类型，可以用 ?或 ~代替  
=，这样就可以强制使用通配符或正则表达式进行匹配。__

__包含非字母数字符号的字符串应该用双引号引起来，像示例中那样。对于其他字符串，双引号是可选的，  
但如果字符串的值与保留关键词冲突，会导致语法错误。如果你的字符串包含大写字母，就不会发生这__

##### 种情况。

__使用命令行选项\-n 提供或默认生成的索引组都可以使用group NR 或group NAME进行引用，其中  
NR 为该组从零开始计数的索引编号，NAME为该组名称的一部分。如果整个选区都由一个索引组提供，  
那么关键词group是可选的。在交互模式下，在行首按下回车键可以查看可用组的列表。__

##### 指定选区中的位置

##### 指定选区中的位置时可以使用几种方法：

__1\.固定位置可用\[XX, YY, ZZ\]定义，其中XX，YY和ZZ 为实数。__

__com of ATOM\_EXPR \[pbc\]或 cog of ATOM\_EXPR \[pbc\] 可以计算ATOM\_EXPR 的质心/几何中  
心。如果指定了pbc，会以迭代方式计算中心，以处理ATOM\_EXPR沿周期性边界条件折叠的情况。__

__POSTYPE of ATOM\_EXPR计算 ATOM\_EXPR 中的原子对应的指定位置。POSTYPE 可以是 atom，  
res\_com，res\_cog，mol\_com或 mol\_cog，还可使用可选的前缀 whole\_，part\_ 或 dyn\_。  
whole\_计算整个残基/分子的中心，即使它只有一部分被选中。part\_ 计算选中原子的中心，但  
对于同一残基/分子总是使用相同的原子。所使用的原子从选区允许的最大组中确定。dyn\_严格  
地只计算选中原子的中心。如果没有指定前缀，整个选区默认为part\_，而其他地方则默认为  
whole\_。后者通常适用于在不同工具中选中相同的分子，而前者是速度与直觉行为的折衷（求值  
dyn\_位置会慢于part\_）。  
4\.用于整个选区的ATOM\_EXPR，其处理方式如上面的第 3 条，处理时使用命令行参数\-seltype指  
定的位置类型。__

__基于位置选择原子的选区关键词，比如dist from，默认使用命令行选项\-selrpos指定的位置。可以  
通过在关键词前面添加POSTYPE限定符来改变这一行为。例如，res\_com dist from POS会求值为残  
基质心的距离。在这个例子中，基于计算得到的单个距离值，一个残基中的所有原子会同时被选中或不  
被选中。__

##### 选区中的算术表达式

##### 选区的数值表达式中支持基本的算术求值。支持的操作有加，减，负，乘，除和幂（使用^）。除以零或

##### 其他非法操作的结果未定义。

##### 选区关键词

##### 以下为当前可用的选区关键词。对带加号标记的关键词，可以通过KEYWORD小节获取额外的帮助信息，

##### 其中KEYWORD为该关键词的名称。

##### • 根据整数型性质选择原子的关键词：

__atomnr__

__mol \(synonym for molindex\)__

__molecule \(synonym for molindex\)__

__molindex__

__resid \(synonym for resnr\)__

__residue \(synonym for resindex\)__

__resindex__

__resnr__

__\(在表达式中使用，或类似于atomnr 1 to 5 7 9\)__

- __根据数值性质选择原子的关键词：__

__beta \(synonym for betafactor\)__

__betafactor__

__charge__

__distance fromPOS \[cutoff REAL\]__

__distance fromPOS \[cutoff REAL\]__

__mass__

__mindistance fromPOS\_EXPR \[cutoff REAL\]__

__mindistance fromPOS\_EXPR \[cutoff REAL\]__

__occupancy__

__x__

__y__

__z__

__（在表达式中使用，或类似于occupancy 0\.5 to 1）__

- __根据字符串性质选择原子的关键词：__

__altloc__

__atomname__

__atomtype__

__chain__

__insertcode__

__name \(synonym for atomname\)__

__pdbatomname__

__pdbname \(synonym for pdbatomname\)__

__resname__

__type\(synonym for atomtype\)__

__（用法类似于name PATTERN \[PATTERN\] \.\.\.）__

- __直接选中原子的额外关键词：__

__all__

__insolidangle center POS span POS\_EXPR \[cutoff REAL\]__

__none__

__same KEYWORD as ATOM\_EXPR__

__within REAL of POS\_EXPR__

- __直接求值为位置的关键词：__

__cog of ATOM\_EXPR \[pbc\]__

__com of ATOM\_EXPR \[pbc\]__

__（另可参见《位置》小节）__

##### 374 第 6 章 命令行参考

##### • 额外关键词：

__merge POSEXPR__

__POSEXPR permute P1\.\.\.PN__

__plus POSEXPR__

__根据原子名称选中原子： __atomname__ ， __name__ ， __pdbatomname__ ， __pdbname____

__name  
pdbname  
atomname  
pdbatomname__

__这些关键词根据名称选中原子。根据name选中原子时使用GROMACS的原子命名约定。对于除PDB  
以外的输入文件格式，原子名称会严格按照它们在输入文件中出现的形式进行匹配。对于PDB文件，  
处理以数字开头的 4 字符原子名称时，会先把数字移到末尾再进行匹配（例如，要匹配PDB文件中的  
3HG2，应使用name HG23）。pdbname只能用于PDB输入文件，并基于输入PDB文件中给出的精确  
名称选中原子，不会进行上述的转换。__

__atomname和pdbatomname是以上两个关键词的同义词。__

__基于距离选中原子： __dist__ ， __distance__ ， __mindist__ ， __mindistance__ ， __within____

__distance fromPOS \[cutoff REAL\]  
mindistance fromPOS\_EXPR \[cutoff REAL\]  
within REAL of POS\_EXPR__

__distance和 mindistance计算到给定位置的距离，唯一的区别是 distance只接受单个位置，而  
mindistance可接受任意数目的位置，然后计算到最近位置的距离。within 直接选中到POS\_EXPR的  
距离处于REAL之内的原子。__

__对前两个关键词，可以指定截断距离以加快求值速度：所有大于指定截断距离的返回值都等于截断值。__

__选中立体角内的原子： __insolidangle____

__insolidangle center POS span POS\_EXPR \[cutoff REAL\]__

__此关键词选中从POS（一个求值为单个位置的位置表达式）看去，处于POS\_EXPR中任意位置的REAL  
度（默认为 5 度）之内的原子，即，在以POS为中心，由 POS\_EXPR中的所有位置张成的立体角之内  
的原子。__

__技术上讲，立体角是一些小圆锥体的合集。这些小圆锥体的顶点位于POS，轴线穿过 POS\_EXPR中的一  
个点。对POS\_EXPR中的每一位置都有一个这样的圆锥体。如果某点处于这些圆锥体中的任意一个之内，  
它就处于指定立体角中，从而被选中。截断值决定了圆锥的宽度。^1__

__合并选区： __merge__ ， __plus____

__POSEXPR merge POSEXPR \[stride INT\]  
POSEXPR merge POSEXPR \[merge POSEXPR\.\.\.\]  
POSEXPR plus POSEXPR \[plus POSEXPR\.\.\.\]__

__基本选区关键词只能创建每个原子至多出现一次的选区。merge 和plus选区关键词可用于绕开这一  
限制。二者创建的选区可以包含了自所有给定位置表达式的位置，即使其中有重复。二者的差别在于，  
merge需要两个或以上，所含位置个数相同的选区，其输出包含从各选区中依次选出的输入位置，即，  
其输出类似于A1 B1 A2 B2，依此类推。大小不等的选区也可以使用merge，只要第一个选区的大小是  
第二个的整数倍。stride参数可用于明确地指定这个倍数。plus只是简单地把位置合并在一起，还能  
用于大小不等的选区。这些关键词只在选区级别合法，不能用于任何子表达式。__

__排列选区： __permute____

__permute P1\.\.\.PN__

__默认情况下，所有选区求值的返回形式为递增排序的原子索引。可以通过在表达式后面添加 permute  
P1 P2 \.\.\. PN来改变这种行为。所有Pi应该形成数字 1 到N的一个排列。这个关键词对选区中每个  
包含N个位置的位置块进行排列，这样位置块中的第i个位置会变为第Pi个。注意，排列的是位置而  
不是单个原子。如果选区的大小不是n的整数倍，会导致致命错误。只能对整个选区表达式进行排列，  
而不能对任何子表达式进行排列，即，关键词permute应出现在选区的最后。__

__根据残基编号选中原子： __resid__ ， __residue__ ， __resindex__ ， __resnr____

__resnr  
resid  
resindex  
residue__

__resnr根据输入文件中的残基编号选中原子。resid是resnr的同义词，用于兼容VMD。  
resindex N选择从输入文件开头算起的第 N个残基。如果输入文件中存在重复的编号（例如在多个  
链中），这种方法可以用于唯一地标识残基。residue是resindex 的同义词。这样可以保证same  
residue as运行正常。__

__扩展选区： __same____

__same KEYWORD as ATOM\_EXPR__

__关键词 same 可用于根据原子表达式的性质扩展选区中的原子。只要一个原子的给定 KEYWORD与  
ATOM\_EXPR中的任意原子匹配，这个原子就会被选中。支持求值为整数或字符串值的关键词。__

##### 选区求值和优化

##### 逻辑求值从左向右进行并使用短路规则，即，一旦知道了某一原子被选中与否，根本不会对其余的表达

##### 式进行求值。这个特性可用于优化选区：在逻辑表达式中，你应该首先写出最严格和/或最不耗时的表达

##### 式。动态和静态表达式之间的相对顺序无关紧要：所有静态表达式只在第一帧之前求值一次，其结果将

##### 成为最左边的表达式。

##### 优化的另一个要点是公用子表达式：它们不会被自动识别，但可通过使用变量手动进行优化。对于复杂

##### 的选区，这会对性能产生非常大的影响，尤其是当你像下面那样定义了几个索引组的时候：

__rdist=distance fromcom of resnr 1 to 5 ;  
resname RES and rdist< 2 ;  
resname RES and rdist< 4 ;  
resname RES and rdist< 6 ;__

__如果不设置变量，这些距离会计算三次，尽管在每个选区中它们都是完全相同的。任何赋值给变量的内  
容都会成为公用子表达式，在每帧内只求值一次。目前，在某些情况下，使用变量实际上会导致轻微的  
性能损失，因为需要进行检查以确定表达式已经对哪些原子进行过求值，但这应该不是太大的问题。__

##### 选区的限制

- __某些分析程序需要的输入选区可能具有特殊的结构（例如，gmx gangle的某些选项要求索引组由  
包含三或四个原子的组构成）。对于此类程序，用户需要提供合适的，总能返回需要位置的选区表  
达式。__
- __所有选区关键词都以递增顺序选中原子，即，你可以把它们当作集合操作，在执行结束后按数值排  
序返回原子。例如，以下选区会以同样的顺序选中相同的原子：__

__resname RA RB RC__

__resname RB RC RA__

__atomnr 10111213__

__atomnr 12131011__

__atomnr 10 to 13__

__atomnr 13 to 10__

__如果需要原子/位置具有不同的顺序，你可以：__

____\-__ 使用外部索引组（对于某些静态选区），  
__\-__ 使用permute关键词来改变最终顺序，或  
__\-__ 使用merge或plus关键词将多个不同选区组成最终选区。__

- __由于技术原因，当表达式的第一个值为负数的时候，像这样__

__charge\- 1 to\-0\.7__

__会导致语法报错。一个变通的解决办法是写成__

__charge \{\- 1 to\-0\.7\}__

__来代替。__

- __当name选区关键词用于PDB输入文件时，输出行为可能不符合直觉。当GROMACS读入一个  
PDB文件时，会将以数字开头的 4 字符原子名称进行转换，例如，1HG2会转换成HG21，而后者  
才是name关键词的匹配目标。使用pdbname可以匹配输入PDB文件中本来的原子名称。__

##### 选区示例

##### 以下，给出不同类型选区使用方法的示例。

##### • 选中所有水中的氧原子：

__resname SOL and name OW__

- __残基 1 到 5 ，残基 10 的质心：__

__res\_com of resnr 1 to 510__

- __距固定位置超过1 nm的所有原子：__

__not within 1 of \[1\.2,3\.1,2\.4\]__

- __属于残基LIG并距蛋白质0\.5 nm以内的所有原子（使用自定义名称）:__

__"Close to protein"resname LIG and within0\.5of group"Protein"__

- __至少有一个原子距残基LIG0\.5 nm以内的所有蛋白质残基：__

__group"Protein" and same residue as within0\.5of resname LIG__

- __质心距残基总质心介于 2 和4 nm之间的所有RES残基：__

__rdist=res\_com distance fromcom of resname RES__

__resname RES and rdist>= 2 and rdist<= 4__

- __包含重复原子的选区，如C1 C2 C2 C3 C3 C4 \.\.\.C8 C9:__

__name"C\[1\-8\]"merge name"C\[2\-9\]"__

__这可用于gmx distance来计算C1\-C2，C2\-C3等原子之间的距离。__

- __具有C2 C1顺序的选区：__

__name C1 C2 permute 21__

__这可用于gmx gangle以得到C2\->C1向量而不是C1\->C2向量。__

- __由两个索引组的质心组成的选区：__

__com of group 1 plus com of group 2__

__这可用于gmx distance以计算两个质心间的距离。__

- __沿x方向的固定向量（可用作gmx gangle 的参考）:__

__\[ 0 , 0 , 0 \] plus \[ 1 , 0 , 0 \]__

- __以下示例解释了各种位置类型之间的差异。这个选区在每个残基选中一个位置，只要三个原子  
C\[123\]中的任意一个满足x < 2。这个位置为所有三个原子的质心。只使用res\_com of时，这  
是默认行为。__

__part\_res\_com of name C1 C2 C3 and x< 2__

__下面这个选区类似，但位置是整个残基的质心：__

__whole\_res\_com of name C1 C2 C3 and x< 2__

__最后，下面这个选区选中同样的残基，但位置是那些严格满足x < 2条件的原子的质心：__

__dyn\_res\_com of name C1 C2 C3 and x< 2__

- __不使用of关键词时，默认行为会与以上所述不同，但除此以外规则是相同的：__

__name C1 C2 C3 and res\_com x< 2__

__就像指定了whole\_res\_com一样工作，并从质心满足x < 2的残基中选中那三个原子。使用：__

__name C1 C2 C3 and part\_res\_com x< 2__

__会基于从C\[123\]原子计算的质心来选中残基。__

## 第 7 章

### 发布注记

##### 这些发行注记记录了GROMACS所有主发布和补丁发布中的变化。主发布包含对所支持功能的变化，

##### 而补丁发布只含对相应主发布中存在问题的修复。

__任何时候都有两个Gromacs版本系列处于活跃维护状态，且处于支持期内。在 2023 年，它们是 2023  
系列和 2022 系列。对于后者，只会进行非常保守的修复，而且只解决影响科学正确性的问题。自然，其  
中一些发布会在 2022 年之后进行，但我们会在版本名称中保留最初发布的年份，以便用户了解他们的  
版本是多少。这样的修复也会被纳入最近的发布系列，如果合适的话。 2024 发布前后， 2022 系列将将不  
再维护。__

__在这些发布说明中报告的问题编号，可以在该问题编号的问题追踪器↪https://gitlab\.com/gromacs/gromacs/\-/  
issues/上找到更多细节\.__

### 7\.1 GROMACS 2023 系列

#### 7\.1\.1 补丁发布

##### GROMACS 2023\.3 发布注记

##### 该版本于 2023 年 10 月 19 日发布。这些发布注记记录了自上个2023\.2版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2022\.6版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

____mdrun__ 现在可以打印因截断效应造成的压力偏差的估计值__

__在nstlist\-1步中使用固定的配对列表会导致配对相互作用缺失,从而造成轻微的能量漂移，但在某些情  
况下，由于临近截止距离时缺失了LJ相互作用，会导致压力在nstlist\-1步中出现可测量的增加。现在，  
mdrun会打印由于这些缺失的LJ相互作用而导致的压力平均误差。__

__Issue 4861↪https://gitlab\.com/gromacs/gromacs/\-/issues/4861__

##### 现在可以控制因截断效应造成的压力偏差

##### 作为临时解决方案，可以通过将环境变量GMX\_VERLET\_BUFFER\_PRESSURE\_TOLERANCE设

__置为所需的容差（以bar为单位）以限制缺失的LJ相互作用对压力的影响。__

__Issue 4861↪https://gitlab\.com/gromacs/gromacs/\-/issues/4861__

##### AWH 能够读取三维或更高维的用户数据

__在读取维数大于 2 的awh输入数据时出错，导致mdrun无法启动。__

__Issue 4828↪https://gitlab\.com/gromacs/gromacs/\-/issues/4828__

##### 在能量最小化过程中可以 限制一组原子的旋转

##### 将能量最小化与强制旋转结合使用时可避免段错误。

__Issue 4865↪https://gitlab\.com/gromacs/gromacs/\-/issues/4865__

##### 修复 GPU DD 和 CPU 成键相互作用缺失力缓冲清除的问题

##### 在使用区域分解的模拟中,当使用直接GPU通信进行环交换（使用GMX\_ENABLE\_DIRECT\_\-

##### GPU\_COMM变量启用）时，在力的环交换之前不进行力缓冲清除可能会导致不正确的力,特别是对于

##### 在分解阶段CPU计算的成键相互作用不存在，而在之前的分解过程中存在的情况。由于使用GPU环

##### 交换的GPU驻留模拟缺乏动态负载均衡支持，此类错误的可能性大大降低。

__Issue 4858↪https://gitlab\.com/gromacs/gromacs/\-/issues/4858__

__改进无静电或弱静电体系的 __Verlet__ 缓冲区估计__

__对于以LJ相互作用为主的体系,如粗粒化体系，Verlet缓冲区估计可能太小，因为只考虑了势能的一阶  
导数。现在还添加了二阶和三阶导数。这可能会对性能产生轻微的负面影响。__

__Issue 4885↪https://gitlab\.com/gromacs/gromacs/\-/issues/4885__

##### 更新虚拟位点速度以避免约束不稳定

##### 虚拟位点速度仅在写速度时才会重新计算，但仍会对它们进行积分。这会导致错误累积。现在，会定期

##### 更新速度，以避免出现（过）大速度。这可能会导致运行因段错误或区域分解错误而崩溃。请注意，虚

##### 拟位点速度仅用于输出，它们不会影响位置。

__Issue 4879↪https://gitlab\.com/gromacs/gromacs/\-/issues/4879__

__添加 __AppleSilicon GPU__ 上 __OpenCL__ 错误的解决方法__

__修复2023\.2的资源泄漏后，OpenCL在M1 Mac（可能还有其他AppleSilicon GPU）上出现故障。__

__Issue 4852↪https://gitlab\.com/gromacs/gromacs/\-/issues/4852__

__修复 __gmx__ 工具__

##### 修复从 AWH 能量文件中提取的 AWH 数据 XVG 的图例

__为了避免混淆，从gmx awh给出的AWH能量文件中提取的AWH数据文件XVG中的维度图例，现  
在从第二个维度开始（第一列不能有图例）。维度图例也已修改为awh\-dim%d（其中%d为维度编号）。__

__Issue 4873↪https://gitlab\.com/gromacs/gromacs/\-/issues/4873__

##### 正确转储 VSITE2FD 虚拟位点

__以前gmx dump无法处理具有虚拟位点VSITE2FD（具有固定距离的 2 个原子）的体系\.请注意，这不  
会影响模拟。__

__Issue 4845↪https://gitlab\.com/gromacs/gromacs/\-/issues/4845__

##### 修复 DSSP 工具

__修复了gmx dssp工具对Pi螺旋的处理，现在它的输出与原始DSSP v4\.1\+相同。__

__Issue 4811↪https://gitlab\.com/gromacs/gromacs/\-/issues/4811__

__修复 __editconf \-d \-noc____

__现在，运行gmx editconf \-noc \-d时可以正确输出单位晶胞向量，这会将盒子大小设置为体系的最大  
尺寸，但不居中。__

__Issue 4875↪https://gitlab\.com/gromacs/gromacs/\-/issues/4875__

__修复 __gmx traj__ 中转动能的计算__

__现在使用gmx traj \-ekr ekr\.xvg计算转动能可以返回正确的结果。__

__Issue 4889↪https://gitlab\.com/gromacs/gromacs/\-/issues/4889__

##### 影响可移植性的修复

____GROMACS__ 可以使用带有 __libc\+\+__ 标准库的 __Clang 16__ 进行编译__

__与libstd\+\+不同，libc\+\+更严格地遵循C\+\+标准，因此不提供已移除的标准库类。为了能够使用  
Clang 16和libc\+\+编译GROMACS，旧符号已替换为捆绑的clFFT源码中的现代C\+\+17等效符号。  
该问题仅影响GROMACS的OpenCL构建。__

____GROMACS__ 自动在新布局中查找 __oneAPI__ 库__

__在oneAPI 2023\.2中重新组织了MKL和SYCL支持库。现在，GROMACS会自动在新旧布局中查找  
所需的库。__

##### 杂项

##### 修复 VMD 插件的编译

##### 因路径处理的改变导致出现了这个问题。

__修复 Issue 4832↪https://gitlab\.com/gromacs/gromacs/\-/issues/4832__

__预处理时拒绝不受支持的各向异性 __C\-rescale____

__此压力耦合设置之前会导致模拟运行时出现错误。__

__修复 Issue 4847↪https://gitlab\.com/gromacs/gromacs/\-/issues/4847__

__修复 __CUDA Graph__ 与邻区搜索步骤相关的问题__

##### 使用试验性的CUDA图形功能时，以前的代码会因以下原因而崩溃：运行时涉及维里计算的步骤与邻

##### 区搜索\(NS\)步骤不一致\-通过确保CUDA图形在维里步骤上适当更新可以解决此问题；运行时在NS

##### 步骤后立即激活CUDA图形\-通过在NS步骤开始处添加必要的同步可以解决此问题；运行时使用奇

__数nstlist值\-这是通过强制图形重新实例化而不是图形更新来修复的，在这种情况下，可以正确地将奇  
数/偶数修剪模式捕获到图形中。__

__修复 Issue 4813↪https://gitlab\.com/gromacs/gromacs/\-/issues/4813__

__修复 __constr\_vsiten__ 中的速度矢量复制__

__修复了constr\_vsiten函数中的速度矢量复制，因为能量最小化不需要速度矢量。该修复避免了复制空  
向量和相应的段错误。__

__Fixes Issue 4814↪https://gitlab\.com/gromacs/gromacs/\-/issues/4814__

__解决使用 __ROCm 5\.5__ 或更高版本时 __AMD MI250X__ 上的性能回归问题__

__与ROCm 5\.3相比，在ROCm 5\.5和5\.6中，某些NBNXM内核在MI250X上出现了高达23%的性  
能下降。我们从 2024 分支向后移植了两个补丁，基本减轻了这种效应。使用ROCm 5\.5\+时仍可能出  
现2%左右的降低。__

__Issue 4874↪https://gitlab\.com/gromacs/gromacs/\-/issues/4874__

##### GROMACS 2023\.2 发布注记

##### 该版本于 2023 年 7 月 12 日发布。这些发布注记记录了自上个2023\.1版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2022\.6版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

__修复仅对 __LJ\-14__ 参数进行微扰时 __mdrun__ 出现的段错误__

__Issue 4769↪https://gitlab\.com/gromacs/gromacs/\-/issues/4769__

##### 修复自由能和 LJ\-PME 的数值不稳定性

__如果计算自由能时使用PME处理Lennard\-Jones相互作用，当两个原子距离较近时，大的舍入误差会  
导致不稳定。__

__Issue 4780↪https://gitlab\.com/gromacs/gromacs/\-/issues/4780__

__修复 __mdrun__ 区域分解最多 __715827882__ 个原子的限制__

__区域分解网格设置中的溢出将可模拟的最大原子数限制为max\_int/3，除非指定了\-dd选项。__

__Issue 4627↪https://gitlab\.com/gromacs/gromacs/\-/issues/4627__

##### 允许键成对相互作用缺失

__使用\-noddcheck时候，mdrun不允许键成对相互作用缺失。现在重新可以这样做了。__

__Issue 4787↪https://gitlab\.com/gromacs/gromacs/\-/issues/4787__

##### 增加并检查输出文件中的原子计数限制

__检查点和trr文件中的最大原子数为715 827 882，现已增加到1 431 655 765个原子。现在，当超出这  
些限制时，mdrun会退出并显示明确的错误消息。对于XTC文件，该限制是通过单独的修复提高的。__

__Issue 4627↪https://gitlab\.com/gromacs/gromacs/\-/issues/4627__

##### 修复退火和多个 T 耦合组的断言失败

__Issue 4800↪https://gitlab\.com/gromacs/gromacs/\-/issues/4800__

##### 正确更新备份的检查点文件

__在 2023 和2023\.1中，从未重写state\_prev\.cpt文件，因此其中始终为运行的第一个检查点。__

__Issue 4810↪https://gitlab\.com/gromacs/gromacs/\-/issues/4810__

##### 修复具有长距离成键相互作用的区域分解

__当使用区域分解并且成键相互作用涉及的距离大于成对列表截断时，mdrun会退出并显示缺少成键相互  
作用的错误。__

__Issue 4818↪https://gitlab\.com/gromacs/gromacs/\-/issues/4818__

__修复 __gmx__ 工具__

__避免工具读取能量最小化的 __tpr__ 文件时出现错误__

__当读取tpr文件时,若其中的积分器设置为能量最小化, NM或TPI，许多工具会退出并显示错误“No v  
in input file”。__

__Issue 4774↪https://gitlab\.com/gromacs/gromacs/\-/issues/4774__

##### 现在当读取的 PDB 用作输入时，工具会保留链标识符

__Issue 4776↪https://gitlab\.com/gromacs/gromacs/\-/issues/4776__

____gmx hbond__ 工具可能产生随机输出__

__由于内存未初始化，gmx hbond工具可能产生随机输出。这不能忽视。还修复了\-ac和\-life选项的问题。__

__Issue 4801↪https://gitlab\.com/gromacs/gromacs/\-/issues/4801__

##### 影响可移植性的修复

____CMake__ 配置包__

__根据构建环境，GROMACS 2023和2023\.1可能会在 prefix /share/cmake/gromacs $SUFFIX /中安装格  
式错误的gromacs\-config\.cmake文件，可能会导致CMake命令find\_package\(gromacs\)失败。__

- __rocfft不再是公共依赖。__
- __如果相关的话,配置包文件现在完全依赖于hipSYCL \(Open SYCL\)。  
Issue 4793↪https://gitlab\.com/gromacs/gromacs/\-/issues/4793, Issue 4797↪https://gitlab\.com/gromacs/gromacs/\-/issues/4797__

##### 杂项

____gmxapi\.commandline\_operation__ 环境变量过滤__

__一个新的实用程序\(gmxapi\.runtime\.filtered\_mpi\_environ\(\)\)可用于从中 os\.environ↪https://docs\.  
python\.org/3/library/os\.html\#os\.environ删除与MPI相关的环境变量,例如准备gmxapi\.commandline\_operation  
的子进程环境\.__

__这是 Issue 4423↪https://gitlab\.com/gromacs/gromacs/\-/issues/4423的后续,原来的修复看起来不够\.__

__Issue 4736↪https://gitlab\.com/gromacs/gromacs/\-/issues/4736__

__对 gmxapi 运行时参数进行依赖于构建的检查__

__根据构建的GROMACS支持MPI还是支持线程MPI，某些/onlinehelp/gmx\-mdrun选项未定义。这__

__类错误可能仅出现在MD日志文件中，因此在使用API的情况下很难确认。__

__向 gmxapi\.simulation\.workflow\.from\_tpr\(\) 添加了额外的检查, 以尝试预防用户错误, 并向__

__gmxapi\.mdrun添加了额外的使用说明\.__

__Issue 4771↪https://gitlab\.com/gromacs/gromacs/\-/issues/4771__

__gmxapi\.mdrun 任务唯一性__

__修复了所有gmxapi\.mdrun模拟任务具有相同ID（和工作目录）的错误\.__

__Issue 4795↪https://gitlab\.com/gromacs/gromacs/\-/issues/4795__

##### 修复多 GPU 上启用 CUDA 图形时崩溃的问题

##### 版本2023\.1中引入了一个错误，导致在多GPU上启用非默认的CUDA图形试验功能时崩溃，这是由

##### 于引入了额外的同步,而CUDA图形代码路径不需要导致的。通过在使用图形时避免同步此版本修复了

##### 这个问题。

__Issue 4786↪https://gitlab\.com/gromacs/gromacs/\-/issues/4786__

##### XTC 支持巨型体系

##### （旧的）XTC格式使用内部字符缓冲区，其尺寸（以字节为单位）作为整数存储在文件中，当存储体系

##### 的原子数目超过大约 3 亿时会导致崩溃。通过仅针对大型体系引入 64 位尺寸,并在XTC标头中使用不

##### 同的幻数\(2023\)此版本解决了这个问题。修复只会改变大型体系的XTC格式（无论如何都会导致旧版

##### 本崩溃）。短期内，外部工具可能无法读取大型体系的XTC文件（会收到幻数不正确的错误），但我们

##### 正在使用外部包来更新其实现。

__Issue 4628↪https://gitlab\.com/gromacs/gromacs/\-/issues/4628__

__修复 OpenCL 中的资源泄漏__

__当在GPU上运行时，使用OpenCL构建的gmx mdrun会慢慢泄漏内存。现在已经修复了。__

__Issue 4807↪https://gitlab\.com/gromacs/gromacs/\-/issues/4807__

__convert\-tpr 可以分配初始速度__

__像自由能这样的系综项目,有时每个体系会依赖于数千次模拟，为方便这样的项目,现在Convert\-tpr可__

__以分配一组新的随机速度，而不是使用grompp重新生成完整的tpr。还修复了一个错误，即在mdp文__

__件中使用 0 作为速度种子与使用\-1具有相同的效果，并导致从操作系统生成新种子。__

__Issue 4809↪https://gitlab\.com/gromacs/gromacs/\-/issues/4809__

__Nosé\-Hoover 恒温器的正确公式__

__说明Nosé\-Hoover温度耦合的几个公式存在不一致之处。更新了参考手册以符合实际的实现。__

__Issue 4695↪https://gitlab\.com/gromacs/gromacs/\-/issues/4695__

__修复损坏的 gcc 版本上的命令行测试__

__gcc 9\.3\.1无法生成正确的路径以进行对比，从而导致测试失败。__

__Issue 4785↪https://gitlab\.com/gromacs/gromacs/\-/issues/4785__

__修复 AMD Zen 4 / Genoa 上的 SIMD 检测 / 推荐__

__Zen 4提供单个AVX\-512单元，但与Intel芯片相比，使用单个AVX\-512单元仍然比使用两个AVX2  
单元更快，这可能是由于更高的时钟频率和更低的指令压力。此更改会在Zen 4上默认选择AVX\-512  
（可以提高性能5\-10%），并且它修改了硬件检测，因此我们只会数算Intel CPU上的AVX单元。它还  
澄清了检测信息，以明确是基于预期性能而不是特定指令集的硬件支持，并确保标准输出消息可以放在  
一行中。  
Issue 4715↪https://gitlab\.com/gromacs/gromacs/\-/issues/4715__

##### GROMACS 2023\.1 发布注记

##### 该版本于 2023 年 4 月 21 日发布。这些发布注记记录了自上个 2023 版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2022\.5版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

__修复 mdrun 可能表现不正确的地方__

##### TPI 和简正模式分析重新支持并行化

__当使用多个MPI进程运行TPI或简正模式分析时，mdrun会退出并出现断言失败。__

__Issue 4770↪https://gitlab\.com/gromacs/gromacs/\-/issues/4770__

__对自由能 __lambda__ 维度， __AWH__ 度量可能不正确__

__当相同lambda点索引的不同lambda分量具有不同的值时，AWH度量使用dH/dlambda作为输入，该  
输入使用了相对于所有lambda分量的导数。注意，这仅影响度量，而不影响采样或自由能值。__

__Issue 4730↪https://gitlab\.com/gromacs/gromacs/\-/issues/4730__

##### 修复使用区域分解时扩展系综模拟的检查点问题

##### 现在，运行多个PP进程时，扩展系综模拟可以从检查点重新启动。

__Issue 4629↪https://gitlab\.com/gromacs/gromacs/\-/issues/4629__

##### 修复 SYCL 中的 PME 管道支持

##### 当使用PME管道时，SYCL中的长程PME静电不正确。

##### 只有使用>=3个GPU并启用直接GPU通信\(GMX\_ENABLE\_DIRECT\_GPU\_COMM环境变量\)时,运行才会

##### 受到影响。

__Issue 4733↪https://gitlab\.com/gromacs/gromacs/\-/issues/4733__

##### 修复维度 > 1 时 AWH 摩擦度量的检查点问题

__对于维度> 1，摩擦度量检查点i/o是错误的。这不会影响AWH PMF或采样，但如果使用AWH摩擦  
张量来计算维度> 1中的扩散，会导致无意义结果。__

__Issue 4723↪https://gitlab\.com/gromacs/gromacs/\-/issues/4723__

__修复 __gmx__ 工具__

__修复 __PDB__ 格式中使用溶剂盒子时 __gmx solvate__ 崩溃的问题__

__现在可以将PDB文件传递给gmx solvate的\-cs选项\.在之前的版本中（至少从 2016 起），会导致  
段错误\.__

##### 修复从另一个索引文件创建索引文件

__gmx make\_ndx可以重新使用单独索引文件作为输入，而不需要关联的结构文件。__

__Issue 4717↪https://gitlab\.com/gromacs/gromacs/\-/issues/4717__

__允许使用 __gmx energy__ 中的完整名称选择能量项__

__现在可以使用完整名称选择能量项。对于以数字开头的项特别有用，例如“1/Viscosity”或“2CosZ\*Vel\-X”，  
以前只能使用编号才能可靠地选择这些项。__

__Issue 4739↪https://gitlab\.com/gromacs/gromacs/\-/issues/4739__

__修复 __gmx anaeig__ 中的早期崩溃__

##### GROMACS 2023中的内部变化使得对可选程序参数的处理不当，从而导致程序崩溃。这可能也会影响

##### 其他一些分析工具。

__Issue 4756↪https://gitlab\.com/gromacs/gromacs/\-/issues/4756__

##### 影响可移植性的修复

__修复 __GMX\_USE\_TNG=off__ 构建__

##### 可以重新在不支持TNG的情况下构建GROMACS。

__修复 __gmx__ 启动期间异常终止__

__GROMACS调用std::filesystem::equivalent的方式不太稳健。当构建目录不再存在时，会导致链  
接到（非典型）libc\+\+标准库的gmx停止执行。__

__Issue 4724↪https://gitlab\.com/gromacs/gromacs/\-/issues/4724__

##### 修复使用 MKL 2023\.0 的 CPU FFT

__此前，使用oneMKL 2023\.0编译的GROMACS在初始化CPU FFT过程中会失败。现在已经修复了这  
个问题。__

__Issue 4691↪https://gitlab\.com/gromacs/gromacs/\-/issues/4691__

##### 杂项

##### 解决奇怪的编译器行为以提高 SYCL 成键内核性能

__对于某些SYCL目标（最值得注意的是，具有ROCm 5\.x的AMD GPU所用的hipSYCL），生成了非  
常低效的成键内核代码。现在，GPU上的成键力的计算速度预计提高到原来的 3 倍。__

__Issue 3928↪https://gitlab\.com/gromacs/gromacs/\-/issues/3928__

__回复牵引例程的 __OpenMP__ 加速__

__在内部代码重组期间，GROMACS 2023中的牵引力计算意外地禁用了OpenMP加速。现已修复。__

__Issue 4747↪https://gitlab\.com/gromacs/gromacs/\-/issues/4747__

__添加了对新 __cuFFTMp__ 接口的支持__

__cuFFTMp库的接口已更改到NVIDIA HPC SDK 23\.3版本中的最新发行，这是支持NVIDIA Hopper  
GPU所必需的。我们现在已为新接口添加了默认支持，同时保留了对旧接口的支持。__

__Issue 4731↪https://gitlab\.com/gromacs/gromacs/\-/issues/4731__

##### 记录 MPI 检测失败时的解决方法

__即使构建不支持MPI库的GROMACS，MPI也是gmxapi的可选依赖项。CMake查找MPI的机制在  
遇到损坏的MPI安装时可能会出问题,方式令人困惑。现在记录了一种解决方法，以方便不打算使用  
MPI的用户。__

__Issue 4699↪https://gitlab\.com/gromacs/gromacs/\-/issues/4699__

#### 7\.1\.2 主发布

##### 亮点

##### GROMACS 2023于 2023 年 2 月 6 日发布，此后可能会有补丁发布，请使用更新的版本\!以下是你可以

##### 期待的一些亮点，相应链接中的有更多细节\!

##### 像往常一样，我们有一些有用的性能改进，无论是否有GPU，都会默认自动启用。此外，还有用于运行

##### 模拟的几个新功能。我们极其希望得到您的反馈，看看新发布在您的模拟和硬件上运行情况如何。这些

##### 新功能包括：

##### • SYCL GPU实现是支持所有主要GPU平台的GPU可移植层，在支持平台和功能方面都有了重

##### 大扩展。为了确保实际使用中的可移植性，积极开发了GROMACS GPU可移植层的多种SYCL

__实现（hipSYCL、oneAPI DPC\+\+、IntelLLVM），并定期对多个GPU后端进行测试。__

____\-__ SYCL支持更多GPU卸载功能：成键力以及使用GPU感知MPI进行直接GPU\-GPU通  
信。  
__\-__ SYCL硬件支持包括AMD（包括此处添加的RDNA支持）和用于生产的Intel以及NVIDIA  
GPU（不用于生产）。  
__\-__ 针对重要HPC平台的SYCL优化。__

- __优化和扩展了PME分解，以支持将整个PME计算卸载到多个GPU上，包括FFT计算；与  
cuFFTmp或heFFTe结合使用时，可以大大改进强时间标度（试验功能）。__
- __添加了CUDA Graph支持，可以完全在GPU上使用线程MPI执行GPU驻留的单/多GPU模  
拟，以提高性能（试验功能）。__
- __现在可以通过OpenCL GPU后端支持Apple M1/M2 GPU。__
- __新的系综温度mdp选项可用于设置系综温度以进行模拟，无需温度耦合或使用不同的参考温度。__
- __借助gmx dssp，GROMACS现在有了DSSP算法的原生实现，它取代了gmx do\_dssp\.__

##### 新特性和改进特性

____mdrun__ 现在还会报告具有 __AWH__ 偏差共享的守恒能量量__

____Added__ 添加了设置系综温度的选项__

##### 压力耦合和AWH等多种算法需要体系的温度。当并非所有原子都耦合到（相同）温度时，现在可以使

__用两个新的mdp选项告知mdrun系综温度的值。__

__Issue 3854↪https://gitlab\.com/gromacs/gromacs/\-/issues/3854__

____gmxapi\.mdrun__ 现在可以给出模拟的工作目录路径__

__gmxapi\.mdrun\(\)\.output\.directory提供模拟\(将使用\)的工作目录的路径\.可以与gmxapi\.utility\.  
join\_path\(\)结合起来以表达数据流\. 这样数据流是基于用户已知的模拟要产生的文件,而不是由  
OutputDataProxy的其他已有属性来表示\.__

__Issue 4548↪https://gitlab\.com/gromacs/gromacs/\-/issues/4548__

____gmxapi\.mdrun__ 现在可以捕获 __STDOUT__ 和 __STDERR____

##### GROMACS库会将大量输出直接打印到标准输出和标准错误。以前，这意味着传统终端中的模拟输出必

__须从Python解释器外部捕获。在基于mpi4py的集成中，在不操作mpiexec命令行的情况下捕获输出  
可能具有挑战性。__

__gmxapi\.mdrun现在可以在模拟过程中重定向STDERR和STDOUT，并在新的 stdout 和 stderr 输出  
上提供结果文本文件的路径。__

##### 性能改进

##### 默认情况下更新将在 GPU 上运行

__如果支持，mdrun\-update auto会默认映射到GPU。对单MPI进程这可以显着提高性能。__

##### 增加默认的温度耦合和压力耦合的间隔

__温度和压力耦合间隔是默认最大值从 10 步增加到 100 步。当在mdp文件中指定默认值\-1时，会使用  
这些值；当需要精确积分时，会使用较低的值。这提高了GPU运行和并行运行的性能。__

__全局通讯频率与 __nstlist__ 无关__

__全局通信频率不再依赖于nstlist。对提高GPU模拟的性能尤其重要。__

##### CUDA 和 SYCL 后端支持 PME 分解

__CUDA和SYCL后端支持PME分解。随着PME卸载到GPU，现在可以使用\-npme选项配置PME  
线程的数目（之前限制为 1 ）。该实现需要在构建GROMACS时使用GPU感知的MPI,以及CUDA构  
建配置中的cuFFTMp库或是CUDA或SYCL构建配置中的heFFTe。__

__基于GPU的PME分解支持仍然缺乏大量测试，因此是作为试验性功能包含在当前发布中的，应谨慎  
使用（与使用单个PME GPU运行的结果进行比较）。可以使用GMX\_GPU\_PME\_DECOMPOSITION环境变  
量启用此功能\.开发团队欢迎任何反馈意见，以帮助完善此功能。__

__Issue 3884↪https://gitlab\.com/gromacs/gromacs/\-/issues/3884 Issue 4090↪https://gitlab\.com/gromacs/gromacs/\-/issues/4090__

##### GPU 驻留步的 CUDA 图形

##### 引入了新的CUDA功能，可以在每一步上加载GPU活动作为单个CUDA图，而不是调度到多个CUDA

##### 管线的多个活动。它仅适用于已经支持GPU驻留步的情况（其中所有力和更新计算都使用GPU加速）。

##### 通过减少CPU和GPU端调度开销，提高了性能，特别是对于小型情况。可以通过GMX\_CUDA\_GRAPH环

##### 境变量激活此功能。

__Issue 4277↪https://gitlab\.com/gromacs/gromacs/\-/issues/4277__

____VkFFT__ 支持__

__对于AMD GPU，已集成了VkFFT以改进性能。所有非分解PME模拟（单进程或单个单独的PME  
进程）都支持使用此库，使用hipSYCL时可以通过\-DGMX\_GPU\_FFT\_LIBRARY=VKFFT启用。__

__Issue 4052↪https://gitlab\.com/gromacs/gromacs/\-/issues/4052__

##### API 的改变

##### 移除旧的收集标题

__以前，一些旧的API 仅 用于收集其他已安装标题的\#include行。没有提供关于给定功能要包含哪  
些标题的指导。这些冗余标题已移除。依赖\#include "gromacs/module\.h"的客户端软件需要使用更具  
体的\#include "gromacs/module/feature\.h"指令进行更新\.__

__Issue 4487↪https://gitlab\.com/gromacs/gromacs/\-/issues/4487__

##### GROMACS 工具的改进

__gmx do\_dssp 替换为 DSSP 算法的原始实现__

__gmx do\_dssp替换为DSSP 4算法的原生实现\.以前可以使用 gmx do\_dssp \-ver 4获得版本 4 的结  
果\.新工具为gmx dssp\.__

##### 错误修复

__为非均相体系设置正确的 __Verlet__ 缓冲__

__现在使用体系的有效密度来估计Verlet缓冲,有效密度是根据初始坐标计算的。这样可以避免低估（非  
常）不均匀体系的缓冲。__

__Issue 4509↪https://gitlab\.com/gromacs/gromacs/\-/issues/4509__

##### 修复大量原子和线程数的段错误

__当原子数乘以OpenMP线程数大于 2147483647 时，负的原子数可能会导致非法内存访问。__

__Issue 4628↪https://gitlab\.com/gromacs/gromacs/\-/issues/4628__

##### 密度导向模拟归一化

__使用\.mdp选项density\-guided\-simulation\-normalize\-densities = yes,可以将参考密度和模拟  
密度值预先除以它们值的总和。__

__对具有大量负体素值的参考密度会导致令人惊讶的行为：如果体素值的总和小于零，密度开始“排斥”  
蛋白质结构而不是吸引它。负归一化常数会导致体素值的符号变化。__

__为避免这种行为，现在对参考密度进行归一化时，会使用正值的总和，从而确保归一化常数始终为正。__

__除了避免意外行为之外，我们预计这还会导致参考密度和模拟密度之间的绝对差异更小，并对数值稳定  
性带来一些小的好处。__

__此 更 改 会 影 响 体 素 值 存 在 负 值 （通 常 不 包 括 合 成 数 据） 且 使 用  
density\-guided\-simulation\-normalize\-densities = yes 运行的所有模拟，但只会对以下方  
面产生较大影响：第一，以相似度內积作为有效的力常数缩放因子，第二，对所有体素值的总和为负的  
所有相似度。__

____gmxapi Python__ 包避免了不必要的 __MPI__ 初始化__

__MPI的延迟初始化（由于mpi4py↪https://mpi4py\.readthedocs\.io/en/stable/mpi4py\.html\#module\-mpi4py的自动行为）避免  
了以前仅通过导入gmxapi进行的MPI初始化。已发现先前的行为会导致与资源管理库的奇怪交互，例  
如libfabric与gmxapi 0\.3版本在意外时间（如包安装期间）产生交互。__

__Issue 4693↪https://gitlab\.com/gromacs/gromacs/\-/issues/4693__

__对 __rlist__ 之外的微扰排除进行故障安全检查__

__对于自由能计算，使用PME时，涉及至少一个微扰原子的排除非键相互作用不应超出rlist。对此的检  
查可能会出现漏报。现在，检查是安全的，并且当微扰的排除对超出rlist时，总会触发致命错误。__

__Issue 3403↪https://gitlab\.com/gromacs/gromacs/\-/issues/3403 Issue 4321↪https://gitlab\.com/gromacs/gromacs/\-/issues/4321 Issue__

__\(^4461\) ↪https://gitlab\.com/gromacs/gromacs/\-/issues/4461__

##### GROMACS 2023 功能的预期变化

##### GROMACS 2023 中废弃的功能

##### 移除的功能

__移除内置查看器 __gmx view____

##### 此功能很少使用，也没有进行测试，并于 2022 年废弃。

__Issue 4296↪https://gitlab\.com/gromacs/gromacs/\-/issues/4296__

##### 移除一些未维护的实用程序脚本

__scripts/目录中的一些脚本没有随软件包一起安装，也没有维护，而且据我们所知，已经很长时间没有  
使用了。__

__Issue 4639↪https://gitlab\.com/gromacs/gromacs/\-/issues/4639__

##### 可移植性

##### 全面支持 RISC\-V

##### 现在全面支持RISC\-V，包括用于高效负载均衡的硬件周期计数器。

__初步支持 Apple silicon GPU__

__现在将Apple设计的GPU视为OpenCL后端支持的架构。__

__VkFFT 通过 OpenCL 和 SYCL 提高 GPU 的可移植性和性能__

__添加了对VkFFT GPU FFT库的支持,有两个目标：提高跨GPU平台的可移植性和更好的性能。  
VkFFT可与OpenCL和SYCL一起使用。对于SYCL构建，VkFFT为AMD和NVIDIA GPU提供  
了一个可移植性后端，并且是一种性能更好的替代方案，建议至少在AMD上进行无PME分解的模拟  
（非HeFFTe构建）时使用。对于OpenCL构建，VkFFT提供了ClFFT的替代方案，具有更好的性能  
和更广泛的编译器支持,是macOS上以及使用Visual Studio构建时的默认设置。在其他平台上，可以  
在构建时使用\-DGMX\_GPU\_FFT\_LIBRARY=VKFFT 启用\.  
Issue 4052↪https://gitlab\.com/gromacs/gromacs/\-/issues/4052__

__macOS 上的 PME GPU 卸载__

__到目前为止，macOS上的PME计算无法卸载到GPU。它们需要clFFT库，该库运行时会与Apple的__

__OpenCL驱动程序发生冲突,悄然崩溃。为了克服不兼容，在macOS上用VkFFT替换了clFFT后端。__

##### 所需版本的增加

##### • 现在GCC所需的版本为9\.

- __现在oneMKL所需是版本为2021\.3。__

##### 7\.1\. GROMACS 2023 系列 397

##### 杂项

##### 修复文档中与限制弯曲势能有关的问题

##### 代码中的实际实现是正确的，但手册中计算限制弯曲势对应力的公式有一个额外的因子2,这个源于

__2013 年Bulacu的JCTC论文，并且两个参考文献的期刊已交换。对任何模拟结果都没有影响。__

__Issue 4568↪https://gitlab\.com/gromacs/gromacs/\-/issues/4568__

##### AWH 行进者之间共享 AWH 摩擦力度量

##### 摩擦力度量现在使用来自所有共享偏置的行进者的数据。在AWH输出中，仅写了共享的摩擦输出。

__Issue 3842↪https://gitlab\.com/gromacs/gromacs/\-/issues/3842__

__要求 __gmx grompp \-maxwarn__ 使用正整数__

##### 以前接受\-1并忽略所有警告。现在必须指定一个正整数。

### 7\.2 GROMACS 2022 系列

#### 7\.2\.1 补丁发布

##### GROMACS 2022\.6 发布注记

##### 该版本于 2023 年 7 月 11 日发布。这些发布注记记录了自上个2022\.5版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2021\.7版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

##### 修复多 GPU 运行中的 CUDA PME 分散问题（使用 >=3 个 GPU ）

##### 由于第二个网格的索引不正确，当使用单独的PME进程并启用管线时，分散可能会出现错误。使用

##### >=3个GPU且启用了直接GPU通信\(GMX\_ENABLE\_DIRECT\_GPU\_COMM环境变量\)的运行会受到影响。

__Issue 4732↪https://gitlab\.com/gromacs/gromacs/\-/issues/4732__

##### 修复 GPU PME 管线中缺少同步

##### 使用GPU PME管线时，缺少同步可能会导致所得的长程PME静电力/能量不正确。

##### 只有使用>=3个GPU并启用直接GPU通信\(GMX\_ENABLE\_DIRECT\_GPU\_COMM环境变量\)的运行才会

##### 受到影响。

__Issue 4734↪https://gitlab\.com/gromacs/gromacs/\-/issues/4734__

__修复 __gmx__ 工具__

##### 影响可移植性的修复

##### 杂项

##### GROMACS 2022\.5 发布注记

##### 该版本于 2023 年 2 月 3 日发布。这些发布注记记录了自上个2022\.4版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2021\.7版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

__修复 __mdrun__ 可能表现不正确的地方__

##### 修复小体系中跨 PBC 的微扰排除处理

##### 对具有多达数百个原子的体系，具有排除微扰原子的分子在周期性边界条件下发生断裂时，可能会在长

##### 距离上重复计算库仑和LJ\-PME相互作用。这导致PME和反应场条件下的能量和力产生非常大的误

##### 差，这可能不会被忽视。使用普通库仑截断时，误差很小并且可能不会注意到。

__Issue 4665↪https://gitlab\.com/gromacs/gromacs/\-/issues/4665__

##### 在 GPU 上运行 PME 时添加缺失的净电荷项

##### 当在GPU上运行PME时，会缺少体系净电荷对应的项。在常规运行中，势能只会增加一个常数，通

__常没有影响。在体系净电荷发生变化的自由能计算中，这会导致不正确的dV/dlambda和Delta lambda  
值（但无论如何应避免通过自由能计算改变体系的净电荷）。__

__Issue 4668↪https://gitlab\.com/gromacs/gromacs/\-/issues/4668__

__外部能量与 __Gapsys__ 软核函数的差异为零__

__这导致所有BAR和AWH非键自由能输出为零，因此错误结果不太可能被忽视。__

__Issue 4705↪https://gitlab\.com/gromacs/gromacs/\-/issues/4705__

##### 修复使用模块化模拟器时扩展系综模拟的检查点

##### 使用模块化模拟器时（这是GROMACS 2022中扩展系综的默认设置），扩展系综模拟会无法写检查

##### 点文件。调查发现了另一个错误，该错误也已修复：从检查点重新启动时，在写入检查点的步骤上发

__生的lambda空间中成功的MC步骤会被忽略。由于检查点一开始就未能写入，因此这不太可能导致  
GROMACS 2022中出现错误结果。__

__模拟重新启动时在检查点步骤上删除成功的MC步骤的错误也存在于旧的代码路径中，这是GROMACS  
2021\.7及更早版本中的默认设置。使用旧代码路径的模拟不再写入检查点文件，并在日志文件中通知此  
行为。__

__Issue 4629↪https://gitlab\.com/gromacs/gromacs/\-/issues/4629__

__修复 __gmx__ 工具__

__影响可移植性的修复__

##### 杂项

__改进 __muParser__ 检测并将内部版本提升至 __v2\.3\.4____

__更新了内部的muParser版本，其中包括我们所做的所有更改。使用muParser的CMake配置来检测外  
部muParser。更新外部muParser所需的版本以匹配内部版本。__

__Issue 4614↪https://gitlab\.com/gromacs/gromacs/\-/issues/4614__

##### GROMACS 2022\.4 发布注记

##### 该版本于 2022 年 11 月 16 日发布。这些发布注记记录了自上个2022\.3版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2021\.6版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

##### GPU 上 1\-4 相互作用的外步能量差不正确

##### 当在GPU上运行自由能计算且不使用区域分解时,若所涉及的原子仅进行电荷微扰而不进行原子类型

__微扰，1\-4相互作用的外部能量差不正确。这个问题并不影响使用couple\-moltype的自由能计算。此  
问题不影响dV/dlambda。如果你使用BAR或AWH进行自由能计算，手动微扰拓扑中的原子电荷,且  
不微扰原子类型，我们建议使用修正后的代码重新运行，以检查结果是否受到此问题的影响。__

__Issue 4616↪https://gitlab\.com/gromacs/gromacs/\-/issues/4616__

____deform__ 选项导致并行 __mdrun__ 退出__

__使用mdp选项deform，当使用多个MPI进程调用时，mdrun将退出并出现MPI错误。__

__Issue 4604↪https://gitlab\.com/gromacs/gromacs/\-/issues/4604__

__牵引时输出平均力会导致 __mdrun__ 写入检查点时退出__

__当pull\_fout\_average设置为yes, gmx mdrun在尝试写入检查点文件时会退出并出现断言失败。__

__Issue 4636↪https://gitlab\.com/gromacs/gromacs/\-/issues/4636__

____AMD RDNA__ 设备现在已被 __OpenCL__ 正确标记为“不支持”__

__AMD RDNA GPU（Radeon RX 5000、 6000 和 7000 系列）从未与OpenCL一起正常工作，通常模拟  
会很快崩溃。我们现在正确地将这些设备标记为不兼容。__

__支持AMD GCN（例如RX Vega 64）和CDNA/CDNA2（例如Instinct MI100）设备。__

__Issue 4521↪https://gitlab\.com/gromacs/gromacs/\-/issues/4521__

__修复 __gmx__ 工具__

__读取大体系 __tpr__ 文件的程序会因随机错误而退出__

__tpr文件的写入和读取代码中包含一个错误，导致读取超过 1 亿个原子的体系时退出并显示随机错误消  
息。__

__Issue 4628↪https://gitlab\.com/gromacs/gromacs/\-/issues/4628__

__使用柔性约束时 __grompp__ 和 __mdrun__ 因断言失败而退出__

__Issue 4605↪https://gitlab\.com/gromacs/gromacs/\-/issues/4605__

__更正了 __gmx awh__ 摩擦度量的图例__

__使用gmx awh \-more输出的摩擦度量为度量的平方根,而图例正则缺少了sqrt\.现已添加\.注意, gmx  
awh \-fric的输出是正确的,不涉及平方根\.__

__Issue 4598↪https://gitlab\.com/gromacs/gromacs/\-/issues/4598__

##### 影响可移植性的修复

##### 杂项

__修复 __nvcc__ 的参数检查__

__对传递给nvcc的标识进行不正确的配置时检查导致多个与性能相关的标识从未被使用。使用Nvidia  
GPU进行的模拟是正确的，但可能未达到最佳性能。__

##### 添加了对新 CUDA 架构的编译支持

__使用默认cmake配置直接生成代码的NVIDIA CUDA架构列表,当使用的编译器中存在支持时,已更新  
为包括最新的Ada Lovelace和Hopper架构。__

##### GROMACS 2022\.3 发布注记

##### 该版本于 2022 年 9 月 2 日发布。这些发布注记记录了自上个2022\.2版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2021\.6版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

__修复 __mdrun__ 可能表现不正确的地方__

##### 在 GPU 上运行时若不使用 DD ，能量最小化不会收敛

##### 当使用GPU进行非键相互作用计算且不使用区域分解时，最速下降和共轭梯度最小化不会收敛。

__Issue 4533↪https://gitlab\.com/gromacs/gromacs/\-/issues/4533__

__只使用 __lambda__ 的副本交换设置被错误地以温度 __\+ lambda__ 分支进行__

__当启用仅lambda模式的副本交换时，副本之间的所有参考温度ref\-t都相同。然而，根据日志消息，会  
使用另一个温度\+lambda分支。__

__Issue 4580↪https://gitlab\.com/gromacs/gromacs/\-/issues/4580__

__修复 __gmx__ 工具__

__修复四面体仲胺的 __pdb2gmx vssite__ 指定__

__对于仲胺这样的结构, pdb2gmx vsite指定代码始终会仅根据原子数为其选择平面型vsite，而不考虑几  
何形状。修复考虑了几何形状。__

__Issue 4573↪https://gitlab\.com/gromacs/gromacs/\-/issues/4573__

__不允许在没有温度耦合的情况下使用 __C\-rescale__ 恒压器__

__C\-rescale恒压器需要一个参考温度,目前是从恒温器获取的。为grompp添加了一个检查,以确定是否存  
在温度耦合或BD/SD。当参考温度不全相同时，也会生成警告。__

__Issue 4495↪https://gitlab\.com/gromacs/gromacs/\-/issues/4495__

__防止 __gmx hbond__ 中的 __hbond__ 合并不兼容的选项__

##### 从一个供体\-受体对合并多个氢键的选项不适用于依赖于分析所有氢键或改变供体\-受体对搜索的其他选

##### 项。因此，如果使用了已知的不兼容组合，该工具会停止。

__当使用\-hbn导出氢键信息并启用合并时，之前会打印任意氢的索引。现在，为避免混淆，索引文件包  
含\-1。如果需要完整的氢键信息，请使用\-nomerge选项。__

__Issue 3837↪https://gitlab\.com/gromacs/gromacs/\-/issues/3837__

##### 修复生成索引时出现重复组

__由于代码中的逻辑错误，gmx make\_ndx和gmx select都会为蛋白质或核苷酸之类的未定义分子重复索  
引组，体系中定义的任何额外组都会导致检测再次运行并生成重复组。__

__Issue 4524↪https://gitlab\.com/gromacs/gromacs/\-/issues/4524__

##### 影响可移植性的修复

__进一步修复 __nvcc__ 标识检测__

__版本2022\.1修复了gcc版本 11 的nvcc标识检测问题，但会导致较旧的gcc版本出现问题。版本2022\.2  
解决了gcc版本 7 的问题，但其他gcc版本仍然存在这个问题。此发布提供了一个修复程序，可以防止  
所有gcc版本出现此问题。__

__Issue 4539↪https://gitlab\.com/gromacs/gromacs/\-/issues/4539__

__记录 __gcc\-11__ 和 __nvcc 11\.6\.1__ 的不兼容性__

__记录了Ubuntu 22\.04上默认gcc和nvcc编译器之间已知的不兼容性，并提供了如何规避该问题的指南。__

__Issue 4574↪https://gitlab\.com/gromacs/gromacs/\-/issues/4574__

##### 杂项

__改进 __mdrun__ 日志文件中的能量输出格式__

__mdrun日志文件现在以缩写形式打印更多能量段名称，以避免超过可用的最大列宽度。__

##### 改进有关 AVX\_128\_FMA SIMD 的警告信息

__该指令集仅适用于支持FMA4扩展的早期AMD CPU。自Zen1以来，AMD转而支持FMA3（类似于  
Intel硬件），不幸的是，这意味着SIMD指令集不是增量的。我们现在对并行运行检查这个问题，并坚  
持使用普通 256 位AVX，并正确检测何时在不兼容的硬件上使用FMA4指令集，并警告运行可能崩溃  
的原因。__

__Issue 4526↪https://gitlab\.com/gromacs/gromacs/\-/issues/4526__

##### 删除 GPU 更新运行时不必要的内存重新分配

##### 修复了启用GPU更新时不必要地重复执行GPU内存分配的问题，这在某些情况下会严重影响性能。

##### 现在仅在必要时才执行内存分配。

##### GROMACS 2022\.2 发布注记

##### 该版本于 2022 年 6 月 16 日发布。这些发布注记记录了自上个2021\.1版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2021\.5版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

##### 修复高度并行运行时的约束错误

__使用区域分解, OpenMP和连接约束（因此不仅是涉及氢原子约束的键）时，若区域不再含有任何以前  
的约束，可以应用约束校正。在较长的运行中，这一点不太可能被忽视，因为原子发生冲突并且体系变  
得不稳定的可能性很高。但短期运行可能不会崩溃，因此可能会产生不正确的结果。正确性可以通过守  
恒能量的漂移来判断，日志文件的末尾会报告漂移值，结果会比正确运行时大一到两个数量级。__

__Issue 4476↪https://gitlab\.com/gromacs/gromacs/\-/issues/4476__

##### 修复自由能计算时缺少 CPU\-GPU 同步的问题

##### 当启用直接通信的GPU环交换时，基于CPU的自由能内核正在运行，而无需等待主机上可用的非本

##### 地坐标。这导致在CPU端使用过时的数据。当使用GMX\_ENABLE\_DIRECT\_GPU\_COMM环境

##### 变量启用GPU直接通信并且模拟涉及自由能计算时，此问题可能会导致不正确的输出。

__Issue 4471↪https://gitlab\.com/gromacs/gromacs/\-/issues/4471__

__修复在单独的 __PME__ 进程上使用 __GPU PME__ 时缺失 __PME__ 网格 __dV/dlambda__ 的问题__

__当在单独PME进程上使用GPU运行PME进行自由能计算时，会缺少PME网格部分对dV/dlambda  
的贡献。外部lambda能量差也缺少同样的贡献。注意，能量和力是正确的。__

__Issue 4474↪https://gitlab\.com/gromacs/gromacs/\-/issues/4474__

__移除 __mdrun \-rerun__ 产生的 __\(__ 不正确 __\)__ 输出文件大小说明 __/__ 警告__

__Issue 4484↪https://gitlab\.com/gromacs/gromacs/\-/issues/4484__

##### 重新初始化后等待 PME 坐标填充清除完成

##### 作为PME坐标缓冲不规则重新初始化的一部分，GPU上缓冲区的填充区域必须设置为零。以前，缺少

##### 依赖，因此，通过GMX\_ENABLE\_DIRECT\_GPU\_COMM启用GPU直接通信时，PME内核可能

##### 会在此初始化完成之前继续执行，现在已修复此问题。错误的执行顺序预计只会发生在极端的基准测试

##### 情况下，从而导致明显的崩溃。

__Issue 4482↪https://gitlab\.com/gromacs/gromacs/\-/issues/4482__

__注意 __Verlet__ 缓冲区估计的已知问题__

__对于非均相体系以及仅具有Lennard\-Jones势的排斥部分的势，Verlet缓冲区估计存在已知问题。这些  
问题和解决方法列在已知问题部分中。__

__Issue 4509↪https://gitlab\.com/gromacs/gromacs/\-/issues/4509__

__修复 __gmx__ 工具__

__澄清了 __pdb2gmx__ 给出的终端数据库中未定义原子类型的错误消息__

__Issue 4481↪https://gitlab\.com/gromacs/gromacs/\-/issues/4481__

__通过能量最小化降低 __grompp__ 排除距离问题的严重性__

##### 通过能量最小化，有关成对距离超出/接近截断距离的错误/警告已更改为警告/注意，因为能量最小化可

##### 能会解决此类问题。

__Issue 4480↪https://gitlab\.com/gromacs/gromacs/\-/issues/4480__

__修复 __:__ 周期性肽缺少 __cmap__ 扭转校正__

__当将pdb2gmx用于周期性肽,且使用CHARMM27力场时，缺少跨周期性边界的CMAP校正（但不是  
扭转本身）。使用2022\.2或更高版本的pdb2gmx重新处理PDB文件以获得正确的拓扑，或手动将其添  
加到拓扑中。__

__避免 __gmx bar__ 因无效输入而崩溃__

__gmx bar可能会尝试读取无效的输入数据文件，并且直接崩溃而不是显示有用的错误消息。__

##### 修复 : 分析工具打印错误数据

##### 处理选区方式的改变导致轨迹分析框架中的分析工具打印错误选区的数据。

__Issue 4508↪https://gitlab\.com/gromacs/gromacs/\-/issues/4508__

__移除 __convert\-tpr__ 中损坏的电荷置零功能__

##### 此功能已经坏了很长时间了，且没有明显的用途。

__Issue 4226↪https://gitlab\.com/gromacs/gromacs/\-/issues/4226__

##### 影响可移植性的修复

__在 __CUDA__ 构建中使用 __gcc__ 版本 __7__ 时发出警告__

__不同版本gcc 7的行为方式不同，这使得GROMACS很难检查CUDA的 nvcc编译器是否接受编译  
器标识。GROMACS 2022和2022\.1有时会错误地将标识检测为无效，避免使用它们，从而生成缓慢的  
CUDA内核。现在，GROMACS假定所有nvcc标识在这种情况下都有效，并且构建系统会在发生这种  
情况时发出警告。如果你随后遇到构建失败，请使用较新版本的gcc。__

__Issue 4478↪https://gitlab\.com/gromacs/gromacs/\-/issues/4478__

__修复 __:__ 外部 __tinyXML__ 版本低于 __7____

__较新的版本与GROMACS不兼容。__

__Issue 4477↪https://gitlab\.com/gromacs/gromacs/\-/issues/4477__

__修复 __: OpenMP__ 链接可能出现的软件构建错误__

__在某些情况下，软件构建链接omp符号时可能会出现错误。对CMake配置的细微更新可帮助muparser  
组件找到与库的其余部分使用的相同OpenMP依赖项。__

__Issue 4499↪https://gitlab\.com/gromacs/gromacs/\-/issues/4499__

##### 杂项

__修复 __:__ 检测外部 __TinyXML\-2____

__更新了代码以正确地检测外部TinyXML\-2的存在和版本（仅在使用\-DGMX\_EXTERNAL\_TINYXML2=ON时  
才相关）。__

__Issue 4477↪https://gitlab\.com/gromacs/gromacs/\-/issues/4477__

__修复 __:__ 使用特定于模块的 __OpenMP__ 线程计数环境变量时的警告__

##### 用于构造消息字符串的数组之一未正确更新，因此有时信息消息是错误的或可能打印出垃圾。

##### GROMACS 2022\.1 发布注记

##### 该版本于 2022 年 4 月 22 日发布。这些发布注记记录了自上个 2022 版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2021\.5版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

##### 开发人员和软件包维护人员请注意

__下一发布 __\(GROMACS 2022\.2\)__ 会将 __master__ 分支重命名为 __main____

__在下一个版本发布时，我们将把master分支重命名为main，以摆脱主/从术语。__

__GROMACS 2022\.2补丁发布后，建议开发人员删除本地master分支并获取远程主分支，如下所示:__

__git branch \-d master; git fetch; git checkout main__

__修复 __mdrun__ 可能表现不正确的地方__

##### 修复 : 测试粒子插入时不正确的配对列表缓冲

__对于TPI，配对列表截断没有考虑rtpi和要插入分子的半径。__

__Issue 4458↪https://gitlab\.com/gromacs/gromacs/\-/issues/4458__

##### 移除自由能内核中缺失排除的误报

##### 自由能计算很好地停止了，出现一个致命错误，指出排除的原子对超出了对列表的截断范围，但实际情

##### 况并非如此。

__Issue 4321↪https://gitlab\.com/gromacs/gromacs/\-/issues/4321__

##### 修复 : 不使用 PME 或使用单独 PME 进程时使用 AWH 导向 FEP 时发生崩溃

##### 在决定是否需要早期PME结果时可能会出现段错误。

__Issue 4413↪https://gitlab\.com/gromacs/gromacs/\-/issues/4413__

##### 修复 : 报告组能量出现错误

##### 当拓扑中一个分子块中的不同分子的原子分配到不同的能量组时，第一个分子的能量组分配将用于块中

##### 的所有其他分子。请注意，报告的整个体系的能量是正确的。

__Issue 4462↪https://gitlab\.com/gromacs/gromacs/\-/issues/4462__

##### 修复 : PME GPU 缺少 B 状态固定

##### 使用GPU PME时，现在可以正确固定PME内存。

__Issue 4408↪https://gitlab\.com/gromacs/gromacs/\-/issues/4408__

##### 只允许 1D PME GPU 分解

##### 由于一维分解PME网格缩减的正确性问题，此功能可能会产生不正确的结果。然而，在大多数现实

##### 情况下，这会被过大的环尺寸所掩盖。0D分解情况不受影响，当前发布中仅允许此类设置（可以使用

##### GMX\_PMEONEDD环境变量强制0D PME分解）。

__修复 __: \-reprod__ 选项的精确延续__

##### 对于蛙跳式积分器，检查点文件中通常不存储动能项。这会导致计算的动能会有微小差异（因操作顺序

__不同），这可能导致从检查点继续运行所得轨迹与不中断运行所得轨迹完全不同，即使使用\-reprod选项  
也是如此。__

__Issue 4240↪https://gitlab\.com/gromacs/gromacs/\-/issues/4240__

__修复 __gmx__ 工具__

__gmx sans 中对氢原子使用正确的散射强度__

__浮点比较总是不成立的，导致所有原子序数为 1 的原子的散射长度为氘的值\(6\.6710 fm\)，而不是普通氢  
的\-3\.7406 fm。__

__修复 __: charmm__ 的 __C__ 末端残留补丁__

__Charmm27力场C末端COOH补丁中的原子类型名称之一不正确，并会触发pdb2gmx的崩溃或错误，  
这是Fedora使用附加检查标识运行我们的单元测试时发现的。__

__Issue 4414↪https://gitlab\.com/gromacs/gromacs/\-/issues/4414__

##### 将聚脯氨酸螺旋着色添加到 DSSP 图

##### DSSP\-4\.0可以检测聚脯氨酸 2 型螺旋，因此现在我们在生成的图中增加了一个深蓝绿色条目。

__Issue 4410↪https://gitlab\.com/gromacs/gromacs/\-/issues/4410__

__移除 __gmx order__ 的 __\-unsat__ 选项及其文档说明__

__自添加以来，此功能尚未正常工作。__

__Issue 1166↪https://gitlab\.com/gromacs/gromacs/\-/issues/1166__

__修复 __: g96__ 文件写入__

__当残基或原子名称超过 5 个字符时，g96文件写入可能会违反文件格式。__

__Issue 4456↪https://gitlab\.com/gromacs/gromacs/\-/issues/4456__

##### 当力过大时，重新运行将不再中止

__Issue 4352↪https://gitlab\.com/gromacs/gromacs/\-/issues/4352__

____extract\-cluster__ 可以使用不完整的索引文件__

__Issue 4420↪https://gitlab\.com/gromacs/gromacs/\-/issues/4420__

##### 影响可移植性的修复

__修复 __: nvcc__ 标志检测__

__Issue 4415↪https://gitlab\.com/gromacs/gromacs/\-/issues/4415__

__修复 __: GMXRC\.bash__ 中的问题__

__Issue 4450↪https://gitlab\.com/gromacs/gromacs/\-/issues/4450__

##### 杂项

##### 修复 : GROMACS 分支回归测试下载的 UR

##### GROMACS分支（如PLUMED）的用户现在也可以使用该功能自动下载回归测试。

__修复 __:__ 内部 __nblib__ 测试失败__

__nblib内部测试使用了不正确的索引，当Fedora使用附加检查标志运行我们的单元测试时，这引发了崩  
溃。这不会影响任何仅使用nblib的实际客户端。__

__Issue 4414↪https://gitlab\.com/gromacs/gromacs/\-/issues/4414__

##### 嵌套 MPI 感知代码的解决方法

__如果任务可执行文件自动检测MPI资源,并且使用MPI启动程序调用脚本，则包含 gmxapi\.  
commandline\_operation任务的gmxapi脚本可能无法使用。__

__解决方法是通过显式设置任务环境变量来增加任务环境与父进程的隔离。现在可以使用commandline\_\-  
operation\(\)的新关键字参数 env 来实现这一点，该参数只是传递给subprocess\.run↪https://docs\.python\.  
org/3/library/subprocess\.html\#subprocess\.run。__

__Issue 4421↪https://gitlab\.com/gromacs/gromacs/\-/issues/4421__

__准确检查 __FEP lambda__ 何时可能超过 __1__ 或低于 __0____

__当delta\-lambda和步数完全正确时，验证FEP lambda未超出范围的检查会被错误地触发。__

__Issue 4442↪https://gitlab\.com/gromacs/gromacs/\-/issues/4442__

##### 正确的自由能（去）耦合积分器检查

__通过自由能（去）耦合计算，grompp只会警告md积分器应使用sd。现在，此警告已扩展到md\-vv积  
分器。__

##### 密度导向模拟的仿射变换力校正

__在计算用于密度导向模拟的力之前，当使用density\-guided\-simulation\-transformation\-matrix进行仿射  
变换,如结构的旋转和投影时，无法正确计算力。__

__出现此错误的原因是缺少与仿射变换矩阵转置的乘法。根据微积分的链式法则，在计算能量的导数以得  
到力时，需要考虑坐标变换。__

__影响设置了density\-guided\-simulation\-transformation\-matrix且并不平凡的模拟。如果矩阵是对角的，  
则力的缩放是错误的。如果设置了旋转矩阵，则会对对力进行错误旋转，从而导致结构上产生不需要的  
整体扭矩。__

__Issue 4455↪https://gitlab\.com/gromacs/gromacs/\-/issues/4455__

##### 澄清了参考手册中的库仑自能项

__Issue 4451↪https://gitlab\.com/gromacs/gromacs/\-/issues/4451__

##### SD 积分器的正确公式

##### 参考手册中的公式与实现不同，尽管两者在数学上是等效的。

##### 调整双精度测试的测试容差

##### 当使用双精度构建时，由于容差过于严格，某些测试在不同的硬件上可能会失败。这主要影响测试模拟，

__由于某些SIMD指令（使用invsqrt时为 44 位）的精度有限，测试模拟可能会出现偏差。__

__Issue 4414↪https://gitlab\.com/gromacs/gromacs/\-/issues/4414__

#### 7\.2\.2 主发布

##### 亮点

##### GROMACS 2022于 2022 年 2 月 22 日发布，此后可能会有补丁发布，请使用更新的版本\!以下是你可

##### 以期待的一些亮点，相应链接中的有更多细节\!

##### 像往常一样，我们有一些有用的性能改进，无论是否有GPU，都会默认自动启用。此外，还有用于运行

##### 模拟的几个新功能。我们极其希望得到您的反馈，看看新发布在您的模拟和硬件上运行情况如何。这些

##### 新功能包括：

##### • 自由能内核使用SIMD进行加速，这使得使用GPU时自由能计算的提速可达三倍以上

##### • 用于自由能计算的软核非键相互作用的新公式能够更精细地控制炼金转化途径

##### • 新的变换牵引坐标能够对一个或多个其他牵引坐标进行任意的数学变换

##### • 用CP2K量子化学软件包进行多尺度量子力学/分子力学（QM/MM）模拟的新接口，支持周期性

##### 边界条件。

- __grompp性能改进__
- __酷炫语录音乐播放列表↪https://open\.spotify\.com/playlist/4oj41X9tgIAJuLgfWPq6ZX__
- __额外的功能移植到模块化模拟器__
- __通过 hipSYCL↪https://github\.com/illuhad/hipSYCL使用SYCL增加了对AMD GPU的支持__
- __使用SYCL支持更多的GPU卸载功能（PME，GPU更新）。__
- __改进了使用CUDA的GPU加速运行的并行化，并扩展了GPU直接通信，以支持使用可感知  
CUDA的MPI进行多节点模拟。__

##### 新特性和改进特性

##### 使用 CP2K 接口的量子 \- 经典混合模拟（ QM/MM ）

##### 模拟化学反应途径可以为许多生物和化学过程提供原子级别的洞察。为了在包括溶剂和/或蛋白质的复

##### 杂体系中进行这种模拟，经常使用多尺度量子力学/分子力学（QM/MM）方法。我们引入了一个全新的

__接口，可以使用MDModule在全周期体系中进行QM/MM模拟，该模块将GROMACS与CP2K量子  
化学包结合起来。这使得可以在发生化学反应的体系中进行混合模拟。该接口支持GROMACS中的大  
多数模拟技术，包括能量最小化、经典MD和增强采样方法，如伞型采样和加速权重直方图法。__

##### 用于牵引坐标数学变换的变换牵引坐标

##### 增加了一个新的牵引坐标类型，称为变换，可以将以前定义的牵引坐标进行数学变换，变换公式来自用

##### 户提供的字符串。这样可以对距离，如接触坐标或多个牵引坐标的（非）线性组合，进行非线性变换。

##### 这是一个定义复杂反应坐标的强大工具，可以与加速权重直方图法结合起来以增强采样。

##### 使用 GPU 更新的副本交换分子动力学模拟

##### 副本交换分子动力学现在可以使用GPU更新。

##### 用于自由能计算的软核相互作用的新公式

__有了这一新增功能，Gromacs可以在炼金扰动期间从两种方案中选择一种来软化非键相互作用。软核函  
数来自Beutler等 100 和Gapsys等185\.__

##### 在 AWH 中更灵活地共享偏差

##### 在加速权重直方图方法中，现在可以在所有模拟的子集之间共享偏差，没有任何限制。这使得可以更灵

##### 活地设置系综模拟，以及更简单地启动一组模拟。

##### 模块化模拟器中实现了更多功能

##### 模块化模拟器增加了一些功能，包括传统模拟器中的所有温度和压力耦合算法，扩展系综和牵引。

##### 自由能计算现在支持所有非微扰的成键相互作用

##### 以前，GROMACS不支持在自由能计算中使用一些更特殊的成键相互作用（限制角/二面角或组合弯

##### 曲\-扭转势）。现在这些都是支持的，只要相互作用本身不会微扰。

__Issue 3691↪https://gitlab\.com/gromacs/gromacs/\-/issues/3691__

##### 根据实际允许的硬件调整线程数

##### 以前，GROMACS会尝试启动的线程数与系统的处理器数目一样，并尝试将线程固着到处理单元上。当

__我们无法使用所有的处理器时，这种作法就会失败，例如，当Slurm只为作业提供了部分节点时，或者  
在A64fx上，一些处理器会留给系统。在容器环境中我们也会启动太多的线程。作为硬件检测改进的一  
部分，我们现在只检测允许运行的处理器，并会在有cpu限制的情况下调整线程的数目，这会提高容器  
的性能，并保证GROMACS在Slurm或其他队列系统分配部分节点时处理正确。__

__允许使用更多的 __OpenMP__ 线程__

__GROMACS中的线程强制缩减代码现在默认允许最多 128 个OpenMP线程，我们已经修改了内部逻  
辑，这样只是限制线程数，而不是拒绝运行。这只适用于每个主线程；你可以将OpenMP线程与多个主  
线程结合以使用不限数目的线程。对于有很多内核的大型机器来说，这通常会更快，因为多个主线程使  
用的区域分解能更好地适应非均匀内存访问硬件。__

__Issue 4370↪https://gitlab\.com/gromacs/gromacs/\-/issues/4370__

____gmx potential__ 中支持居中和对称化__

__gmx potential现在支持与gmx density相同的居中和对称选项，这对膜特别有用。Issue 3579↪https:  
//gitlab\.com/gromacs/gromacs/\-/issues/3579__

##### 性能改进

##### 与 CUDA 感知的 MPI 进行 GPU 直接通信

##### 在NVIDIA GPU上运行时，对直接GPU通信的支持已经扩展到使用CUDA感知的库\-MPI的模拟。

__CUDA感知MPI的检测可在cmake和运行时进行。该功能主要通过OpenMPI进行了测试，但任何  
CUDA感知MPI的实现都应该适用，而且也可以与GROMACS中的线程MPI实现一起使用。CUDA  
感知MPI的支持仍然缺乏实质性的测试，因此在当前的发布中被视为一个开发特性，应谨慎使用。因此，  
即使检测到合适的MPI，默认情况下也不会使用直接通信，但可以使用GMX\_ENABLE\_DIRECT\_\-  
GPU\_COMM环境变量来启用它\.__

__Issue 3960↪https://gitlab\.com/gromacs/gromacs/\-/issues/3960 Issue 2915↪https://gitlab\.com/gromacs/gromacs/\-/issues/2915__

##### 用于能量最小化的动态配对列表生成

##### 对于能量最小化，当并行运行时，如果至少有一个原子的移动超过了配对列表缓冲区大小的一半，就会

##### 执行配对表以及区域分解。以前每步都要构建配对列表。

##### 非键自由能内核使用 SIMD

##### 现在非键自由能内核可以使用SIMD加速，这样自由能计算性能得到了提高。在AVX2\-256上，这些内

##### 核的速度是原来的 4 到 8 倍。对大多数体系而言这应该是一个明显的提速，特别是当微扰相互作用的计

##### 算为瓶颈时。在使用GPU的情况下尤其如此，自由能运行的性能提升可达到 3 倍之多。

__Issue 2875↪https://gitlab\.com/gromacs/gromacs/\-/issues/2875 Issue 742↪https://gitlab\.com/gromacs/gromacs/\-/issues/742__

##### PME\-PP GPU 直接通信流水线化

##### 对于启用了直接PME\-PP GPU通信的多GPU运行，PME进程现在可以将坐标传输与PME扩展和

##### 样条内核中的计算进行流水线处理（这里会使用坐标）。每次传输的数据都是单独处理的，这样计算和

__通信可以同时进行。对于多个GPU之间共享硬件通信接口的系统，如多GPU服务器中的PCIe或跨  
多节点的Infiniband，预期收益最大，__

__Issue 3969↪https://gitlab\.com/gromacs/gromacs/\-/issues/3969__

##### 单个 MPI 进程下的区域分解

__当使用单个MPI进程运行时，如果使用PME并且无GPU，mdrun现在会使用区域分解机制来重新排  
序粒子。这可以提高性能，尤其是对于大型体系。这一行为可以通过环境变量GMX\_DD\_SINGLE\_RANK来  
控制。__

##### 多重时间步进的有限 GPU 支持

##### GPU可以与MTS结合使用，但目前仅限于这样的设置：长程非键力只在较长的时间步长中施加（并在

##### CPU上计算），而所有其他分量每步都计算（可以在GPU上进行）。

__gmx grompp 运行速度提高了 20\-50%__

__经过一系列改进，gmx grompp 参数和原子查找代码中循环的运行速度得到了提高，同时使用了更简单、  
标准的代码习惯\.__

##### 在 CUDA 和进程 MPI 混合模式下支持 PME 分解

##### 在使用CUDA后端的混合模式下，现在支持PME分解。但只有在使用外部进程MPI编译GROMACS，

##### 并且底层MPI实现可以感知CUDA的情况下才支持。该功能缺乏实质性的测试，默认情况下禁用，但

##### 可以通过设置GMX\_GPU\_PME\_DECOMPOSITION=1环境变量来启用\.

__在 __Ampere__ 类 __Nvidia GPU__ 上运行时的性能改进__

##### 将短程非键内核的性能提高了12%\.

__Issue 3872↪https://gitlab\.com/gromacs/gromacs/\-/issues/3872__

##### API 的更改

##### 移除物理常数转换函数

##### 物理常数与GROMACS表示之间的传统转换函数已移除，因为它们在库中没有任何用途。

##### GROMACS 工具的改进

__gmx msd 已迁移到轨迹分析框架中__

__该工具现在使用GROMACS选区语法。使用\-sel选项提供选区，而不是通过标准输入提供选区。添  
加了一个新的选项\-maxtau，用于限制计算MSD时要比较的帧之间的最大时间间隔。这样对大体系进  
行采样时可以将tau值限制在有用的范围内，以避免出现内存不足的错误以及执行缓慢的问题。__

__改写的代码在执行时间上大约有20%的加速。__

__一些很少使用的功能还没有改写，包括:__

- __\-tensor选项还没有实现。__
- __使用\-rmcomm选项移除体系的COM运动尚未实现。__
- __还不支持使用\-pdb选项输出B\-因子。__

__一个轻微的改变是取消了\-mw选项。gmx msd与\-mol的组合会使用分子质心的MSD，当不使用\-mol时，  
不会进行质量加权。在以前的GROMACS版本中，\-mw默认开启，当选择\-mol时，\-nomw会被忽略。  
这一改变只会在不使用”\-mol的情况下，对非均质颗粒组进行MSD计算时，才会导致不同的结果。__

__Issue 2368↪https://gitlab\.com/gromacs/gromacs/\-/issues/2368__

__gmx lie 现在可以从重新运行中读取能量文件__

__这个工具以前依赖于\.edr文件中存在的压力数据。如果\.edr是重新运行得到的，就会缺失这些数据。但  
是，没有必要依赖压力数据的存在，所以现在这个工具可以正常工作。__

__Issue 4070↪https://gitlab\.com/gromacs/gromacs/\-/issues/4070__

__gmx chi 不再需要为自定义残基添加 residuetypes\.dat 条目__

__移除了需要在residuetypes\.dat中添加自定义残基名称的做法，因为不起任何作用。这样gmx chi更  
易使用\.__

__gmx wham 的文本输出进行了微小改进__

__输出文本中报告了正在处理的文件以及输入文件列的内容，这样更容易理解。__

__gmx do\_dssp 支持 DSSP 版本 4__

__do\_dssp可以使用较新的DSSP版本 4 ，只要指定\-ver 4选项，并将DSSP环境变量设置为mkdssp的  
可执行路径\(例如setenv DSSP /opt/dssp/mkdssp\)即可\.__

__Issue 4129↪https://gitlab\.com/gromacs/gromacs/\-/issues/4129__

__gmx trjconv \-dump 可以输出可靠结构__

__现在总会输出最接近－dump指定时刻的帧，即使指定时刻不在轨迹文件中的时间范围之内。为得到轨  
迹文件的最后一帧，如果该文件中的帧是按时间顺序排列的，你可以指定任何一个大于轨迹最大时间的  
值，如gmx trjconv \-dump 9999999\.__

__Issue 2873↪https://gitlab\.com/gromacs/gromacs/\-/issues/2873__

__gmx trjconv 可以更好地处理 TNG 文件中的选区__

__以前在输出TNG文件时，即使用户只要求输出需要的原子选区，仍然会输出整个体系。现在应该只会__

__输出选定的原子。如果选区的名称与某一分子类型相匹配，并且所选原子都存在于该分子中，那么会按__

__预期输出该分子，以及正确的分子数等。如果选区项仅与一个分子中的某些原子或多个分子中的原子相__

__匹配，那么TNG文件中会输出一个包含所有这些原子的单一分子实例。__

__Issue 2785↪https://gitlab\.com/gromacs/gromacs/\-/issues/2785__

__gmx pdb2gmx 不再接受使用 OPLS\-AA 力场的带电谷氨酰胺（ QLN ）__

__对（非标准）带电谷氨酰胺残基，OPLS－AA力场中缺少一个扭转角度参数，Grompp会使用默认的  
扭转角代替。为避免这种静默的错误，从OPLS\-AA力场中删除了带电谷氨酰胺残基。__

__Issue 3054↪https://gitlab\.com/gromacs/gromacs/\-/issues/3054__

__gmxapi\.commandline\_operation 隔离了工作目录__

__为封装的命令行操作而启动的子进程现在运行在唯一的子目录中。使用 output\_files 输入和 file 输出映  
射的用户应该不会受到影响。那些依赖封装命令执行位置假定的用户需要调整他们的脚本。__

__stderr , stdout ,和 file 输出成员仍然是访问命令输出的主要支持方式。此外，新的 directory 输出给出了  
文件系统的路径，可用于子进程。详情见gmxapi\.commandline\_operation\(\)\.__

__Issue 3130↪https://gitlab\.com/gromacs/gromacs/\-/issues/3130__

##### 错误修复

##### 修正了压力耦合下使用虚拟位点时存在的轻微不准确问题

##### 体系演化后虚拟位点会重新构建，但构建是在压力耦合导致的缩放之前进行的。对于不是由其他原子线

##### 性组合而成的虚拟位点类型，这并不完全正确。由于压力耦合引起的缩放在稳定模拟中非常小，因此导

##### 致的不准确性预计极其微小，在大多数情况下无法察觉。

__Issue 3866↪https://gitlab\.com/gromacs/gromacs/\-/issues/3866__

__当 __nstdhdl > nstcalcenergy__ 时输出正确的 __dVremain/dl____

__当nstcalcenergy不是nstdhdl的倍数时，能量文件中会输出错误的dVremain/dl项。请注意，所有  
dH/dl输出，dhdl\.xvg和能量文件中的，现在都是正确的，gmx bar会使用这些文件。__

##### 移除了加速组的速度输出

##### 能量文件中报告的加速组的速度始终是零。现在能量文件中不再报告他们的速度。

__Issue 1354↪https://gitlab\.com/gromacs/gromacs/\-/issues/1354__

____OPLS__ － __AA__ 力场中 __Me2PO4__ 使用正确的 __c0__ 参数__

__OPLS－AA的扭转必须加和为 0 ，但Me2PO4的参数并非如此。已经将c0参数修改为正确的值。__

__Issue 4075↪https://gitlab\.com/gromacs/gromacs/\-/issues/4075__

##### 函数类型傅里叶二面角支持进行自由能微扰

##### 傅里叶二面角（二面角相互作用类型 3 ）不能用于自由能微扰模拟。因为二面角参数终归会转换为

__Ryckaert\-Bellemans参数，所以现在微扰检查对于这两类函数是一样的了。__

__Issue 2606↪https://gitlab\.com/gromacs/gromacs/\-/issues/2606__

__在 __Parrinello\-Rahman__ 压力耦合过程中不再缩放冻结原子的坐标__

__当使用Parrinello\-Rahman压力耦合时，盒子的缩放会用于所有原子，导致冻结原子发生移动。在模拟  
过程中，当压力发生显著变化时，这种影响在盒子两侧的表现更为剧烈。现在，耦合器会忽略冻结原子，  
冻结的原子会保持其冻结维度的值不变。__

__Issue 3075↪https://gitlab\.com/gromacs/gromacs/\-/issues/3075__

##### 在各向异性体系中使用测试粒子插入时避免非均匀旋转

##### 在各向异性体系中，使用随机角度并不会产生均匀分布。

__Issue 3558↪https://gitlab\.com/gromacs/gromacs/\-/issues/3558__

##### 自由能计算可以使用线性键角势

__grompp不会明确允许使用线性键角势进行自由能计算。__

__Issue 3456↪https://gitlab\.com/gromacs/gromacs/\-/issues/3456__

__修正 __trjconv__ 和 __trjcat__ 中的进度显示__

__在trjconv和trjcat轨迹操作过程中显示的进度信息（帧数和时间）现在可以正确地显示。__

__Issue 4320↪https://gitlab\.com/gromacs/gromacs/\-/issues/4320__

##### 修正 GROMOS 力场中二硫键的二面角问题

__对于GROMOS系列力场，pdb2gmx现在可以为二硫键生成正确的二面角。__

__Issue 4188↪https://gitlab\.com/gromacs/gromacs/\-/issues/4188__

##### 修正周期性反常二面角的能量项命名问题

##### 这些能量项内部使用的名称与非周期性二面角的相同，输出到能量文件，从能量文件中读取时都使用了

##### 相同的名称。如果这些项以不同顺序写到文件中，当一些工具试图比较它们时就可能发生错误。

____gmx density__ 现始终使用相对坐标__

__如果盒子大小发生变化，在分格时使用绝对坐标是不现实的，所以现在gmx density内部始终使用相对  
坐标。这也避免了当用户忘记了此选项，输出会缩放到最后的盒子大小而不是平均盒子大小的问题，确  
保输出始终正确，并杜绝了偶尔出现的段错误。__

__Issue 3830↪https://gitlab\.com/gromacs/gromacs/\-/issues/3830__

##### GROMACS 2022 功能的预期变化

##### GROMACS 2022 废弃的功能

__废弃 __GMX\_OPENCL\_NB\_CLUSTER\_SIZE CMake__ 变量 __,__ 使用 __GMX\_GPU\_NB\_CLUSTER\_SIZE____

__OpenCL和SYCL都已支持不同的集群大小，因此应该使用GMX\_GPU\_NB\_CLUSTER\_SIZE\.__

__移除内置查看器 __gmx view____

__此功能很少使用，也没有测试，所以不值得继续维护。__

__Issue 4296↪https://gitlab\.com/gromacs/gromacs/\-/issues/4296__

__移除分析工具 __gmx chi____

##### 此工具已经失效好些年了。如果你对它感兴趣，请在下面链接的问题上发表评论。

__Issue 4108↪https://gitlab\.com/gromacs/gromacs/\-/issues/4108__

##### 废弃根据原子名称猜测质量和原子半径的做法

##### 当需要原子质量或范德华半径时，我们建议构建一个适当的GROMACS拓扑，而不是直接使用PDB

##### 文件，即使该工具支持它。

__Issue 3368↪https://gitlab\.com/gromacs/gromacs/\-/issues/3368 Issue 4288↪https://gitlab\.com/gromacs/gromacs/\-/issues/4288__

##### 移除的功能

__移除仅构建 __mdrun__ 的配置__

__已经不再需要构建只含有mdrun的GROMACS，因为mdrun与常规GROMACS具有相同的依赖关  
系。此功能已在GROMACS 2021中废弃。移除它可以简化维护、测试、文档、安装以及教授新用户。__

__Issue 3808↪https://gitlab\.com/gromacs/gromacs/\-/issues/3808__

__移除对 __x86 MIC__ 、 __ARMv7__ 、 __Sparc64 HPC\-ACE__ 和 __IBM VMX SIMD__ 的支持__

__这些平台已经不在HPC中使用，所以不再支持。KNL平台不受此变化影响。__

__Issue 3891↪https://gitlab\.com/gromacs/gromacs/\-/issues/3891__

##### 移除废弃的环境变量

##### 移除下列已废弃的环境变量，改用更好的名称：

##### • GMX\_CUDA\_NB\_ANA\_EWALD和GMX\_OCL\_NB\_ANA\_EWALD\(换用GMX\_GPU\_NB\_ANA\_EWALD\)

##### • GMX\_CUDA\_NB\_TAB\_EWALD和GMX\_OCL\_NB\_TAB\_EWALD\(换用GMX\_GPU\_NB\_TAB\_EWALD\)

##### • GMX\_CUDA\_NB\_EWALD\_TWINCUT 和 GMX\_OCL\_NB\_EWALD\_TWINCUT \(换 用 GMX\_GPU\_NB\_EWALD\_\-

##### TWINCUT\)

__Issue 3803↪https://gitlab\.com/gromacs/gromacs/\-/issues/3803__

__移除 __gmx wham__ 读取 __\.pdo__ 文件的功能__

__\.pdo格式的文件是GROMACS 4\.0之前的版本输出的。那是很久以前的事了，能够读取它们已经没有必  
要了。所以此功能已在 2021 版本中废弃。如果你确实需要读取这些文件，请使用旧版本的GROMACS。__

##### 移除对 32 位的支持

##### 我们在 2020 版本取消了对 32 位的支持，在那之前的一段时间里，我们已经没有办法自己对它进行测试

##### 了。这些架构在HPC中已不再使用，所以我们正式地不再支持在这些架构上构建GROMACS。

##### 便携性

__不再支持 __Intel__ 经典编译器 __\(icc/icpc\)____

__我们现在支持来自oneAPI的基于英特尔clang的编译器\(icx/icpx\)。请使用它，或gcc。__

__Issue 3893↪https://gitlab\.com/gromacs/gromacs/\-/issues/3893__

##### 暂定：从 BUILD\_SHARED\_LIBS 初始化 GMX\_INSTALL\_NBLIB\_API 和 GMXAPI 构建选项

__CMake选项GMXAPI和GMX\_INSTALL\_NBLIB\_API会生成共享对象库，所以它们的默认值现在由BUILD\_\-  
SHARED\_LIBS初始化。根据 Issue 3605↪https://gitlab\.com/gromacs/gromacs/\-/issues/3605以及相关问题的进展，这些  
选项之间的耦合关系可能会改变，但用户一般不需要手动设置GMXAPI和GMX\_INSTALL\_NBLIB\_API\.__

__Issue 4053↪https://gitlab\.com/gromacs/gromacs/\-/issues/4053__

____pybind11__ 依赖的更新__

__pybind11不再与GROMACS捆绑在一起。__

__gmxapi 0\.3 Python软件包的构建系统依靠PEP 517/518的构建要求，通过Python打包系统获得  
pybind11头文件的依赖关系。像 pip这样的软件包管理器会自动下载依赖项。不自动完成依赖关系的  
软件包管理器仍应向用户报告缺少的依赖关系。__

__sample\_restraint样本项目\(捆绑在python\_packaging/sample\_restraint中\)仍只有一个初步的仅  
由CMak构建的流程。如果你从此源码分叉出一个项目，可以选择现代化的构建系统\(类似于gmxapi的\)  
或捆绑pybind11源代码。在GROMACS资源库中，sample\_restraint选项现在默认为GMXAPI\_\-  
EXTENSION\_DOWNLOAD\_PYBIND=ON\.__

__Issue 4092↪https://gitlab\.com/gromacs/gromacs/\-/issues/4092__

____CMake__ 工具链文件替换为缓存文件__

__不再提供 gromacs\-toolchain\.cmake 文件 \(之前安装到$CMAKE\_INSTALL\_PREFIX/share/cmake/  
gromacs/\)，而是将一个部分的 CMake缓存文件安装到$CMAKE\_INSTALL\_PREFIX/share/cmake/  
gromacs$\{SUFFIX\}/gromacs\-hints\.cmake\.__

__客户端软件可以通过配置 \-C /path/to/gromacs\-hints\.cmake来获得CMake 提示, 而不要使  
用\-DCMAKE\_TOOLCHAIN\_FILE或\-\-toolchain强制进行交叉编译的CMake配置。__

__与GROMACS捆绑的客户端软件（gmxapi Python软件包）不再需要工具链文件。详情见 Full  
installation instructions\.__

__Issue 4208↪https://gitlab\.com/gromacs/gromacs/\-/issues/4208__

__捆绑 __muparser____

__GROMACS现在捆绑了2\.3版本的MuParser。也可以链接到一个外部提供的库。__

##### 杂项

____grompp__ 不再修改 __nstcomm____

__grompp不再设置nstcomm，即移除质心运动的时间间隔，当nstcomm < nstcalcenergy时，其值等于  
nstcalcenergy。在这种情况下，仍会给出注意信息。__

##### 成键原子的类型名称支持以数字开头

##### 拓扑中的成键原子的类型名称以前不允许以数字开头。现在支持所有至少包含一个非数字字符的名称。

__Issue 4120↪https://gitlab\.com/gromacs/gromacs/\-/issues/4120__

____grompp__ 会在可能缺少排除力时发出警告__

__当使用PME时，非微扰原子对之间的排除力应处于截断距离内，否则mdrun可能无法计算网格校正的  
力和能量。grompp现在会使用起始结构计算这些距离，并在它们超过截断距离的90%时发出警告，在  
它们超过截断距离时导致错误。__

__Issue 4051↪https://gitlab\.com/gromacs/gromacs/\-/issues/4051__

##### 角度的 AWH 覆盖直径以度为单位

__使用旧的tpr文件，其中将AWH用于键角或二面角，并且具有非零的覆盖直径，这会导致错误，建议  
重新生成tpr文件。__

__Issue 4367↪https://gitlab\.com/gromacs/gromacs/\-/issues/4367__

##### 移除内核启动代码

__以前，在非x86和非PowerPC平台上，mdrun会运行一些多线程代码，以尝试唤醒操作系统电源可  
能已经关闭的任何内核。在一些Arm平台上这会引起问题，并且导致似乎不适合在大量平台上使用  
GROMACS。所以现移除了相关代码。__

__如果需要，请手动启动内核，如，stress \-\-cpu $\(nproc \-\-all\)\.__

__Issue 4074↪https://gitlab\.com/gromacs/gromacs/\-/issues/4074__

##### 增加线性键角势的文档

__增加了线性键角势的文档和参考。同时添加了please\_cite条目，但目前还没有调用可以引用它。__

__Issue 4286↪https://gitlab\.com/gromacs/gromacs/\-/issues/4286__

____gmxapi\.mdrun__ 会保证轨迹输出__

__gmxapi模拟运行时现在始终以全精度输出轨迹\(\-o\)，以保证通过mdrun\.output\.trajectory结果可用  
输出轨迹的可用性\.__

__Issue 4285↪https://gitlab\.com/gromacs/gromacs/\-/issues/4285__

____gmxapi\.mdrun__ 接受任意的运行时参数__

__任意的mdrun参数都可以通过gmxapi的新的 runtime\_args 关键词来传递，它接受一个含有标识和值  
的字典\.__

__Issue 4284↪https://gitlab\.com/gromacs/gromacs/\-/issues/4284__

__为 __gmxapi Python__ 运行改进了 __MPI__ 感知和任务唯一性__

__以前，只有gmxapi\.simulation中的Python组件会对MPI上下文有反应。这可能导致重复工作，甚  
至是无效的文件访问。__

__gmxapi\.commandline\_operation\(\)现在会在唯一的工作目录中执行任务\.__

__对所有gmxapi操作，任务只从一个进程（对每个系综成员）启动。如果mpi4py↪https://mpi4py\.readthedocs\.io/  
en/stable/可用，就会检查MPI环境。如果发现了多个进程，不同进程的ResourceManager实例会进行协  
调，以确保每个任务的每个成员只会调用update一次。结果会从发生工作的ResourceManager向所有  
进程广播。__

__这些变化仅仅是修复错误。还需要更多的开发，才能更有效地使用资源，并减少不必要的数据传输。__

__Issue 3138↪https://gitlab\.com/gromacs/gromacs/\-/issues/3138__

__进一步鼓励不再使用 __Berendsen__ 耦合算法__

##### 已经证明这些算法会导致对其各自分布进行不正确的采样。提供它们主要是为旧的模拟提供向后的兼容

__性。这就是为什么进一步不鼓励使用它们，grompp时目前关于其使用的注意改为实际警告。__

### 7\.3 GROMACS 2021 系列 \( 自此以下不再维护 \)

#### 7\.3\.1 补丁发布

##### GROMACS 2021\.7 发布注记

##### 该版本于 2023 年 1 月 31 日发布。这些发布注记记录了自上个2021\.6版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2020\.7版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

##### 在 GPU 上运行 PME 时添加缺失的净电荷项

##### 当在GPU上运行PME时，会缺少体系净电荷对应的项。在常规运行中，势能只会增加一个常数，通

__常没有影响。在体系净电荷发生变化的自由能计算中，这会导致不正确的dV/dlambda和Delta lambda  
值（但无论如何应避免通过自由能计算改变体系的净电荷）。__

__Issue 4668↪https://gitlab\.com/gromacs/gromacs/\-/issues/4668__

__修复 __gmx__ 工具__

__影响可移植性的修复__

##### 杂项

##### GROMACS 2021\.6 发布注记

##### 该版本于 2022 年 7 月 8 日发布。这些发布注记记录了自上个2021\.5版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2020\.6版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

__修复 __mdrun__ 可能表现不正确的地方__

__扩展自由能排除超过 __rlist__ 时的错误消息__

__在自由能解耦模拟中，由于盒子太小，可能会出现排除超出rlist的错误。现已将此原因添加到错误消息  
中。__

__Issue 3403↪https://gitlab\.com/gromacs/gromacs/\-/issues/3403 Issue 3808↪https://gitlab\.com/gromacs/gromacs/\-/issues/3808__

##### 修复 : 仅使用 LJ PME 运行

##### 由于任务分配错误，仅使用LJ PME而没有静电PME的模拟会无法运行。

__Issue 4362↪https://gitlab\.com/gromacs/gromacs/\-/issues/4362__

##### 修复 : CUDA 更新内核中缺少同步

__当使用具有SETTLE或LINCS约束的GPU更新时，Volta和较新的NVIDIA GPU上的维里计算可  
能不正确，进而导致压力不正确。默认不启用GPU更新，因此错误只会出现在手动启用的模拟中，即  
使在这种情况下，错误也可能很少见，因为实际上我们在执行测试中没有发现。__

__要检查你的运行是否受到影响，请检查mdrun日志文件：__

- __查找“GPU support: CUDA”行;__
- __查找“PP task will update and constrain coordinates on the GPU”行;__
- __检查是否有任何GPU“GPU Info:”部分中的“compute cap\.”值达到“7\.0或更高。__

__如果这三条都存在，则该错误可能会影响维里计算，进而导致不正确的压力耦合。2021\.6和2022\.0之前  
允许将更新和约束计算卸载到GPU的所有GROMACS版本都会受到影响。__

__Issue 4393↪https://gitlab\.com/gromacs/gromacs/\-/issues/4393__

__修复 __gmx__ 工具__

__gmx rms: 除非需要，否则不要尝试猜测原子名称__

__根据原子名称猜测原子质量有时可能会失败。当使用\-nomw开关时，不需要原子质量，但gmx rms无  
论如何都试图进行猜测，因此当遇到未知元素时就会抛出致命错误。现在，只有当实际需要质量时才会  
出现错误。__

__Issue 4356↪https://gitlab\.com/gromacs/gromacs/\-/issues/4356__

##### 影响可移植性的修复

##### 杂项

##### 更正用户指南中 AWH 间隔的单位

__当将AWH用于角度或二面角时，用户指南mdp部分中列出的采样间隔的键现在以度为单位。指南错  
误地说明以弧度为单位，而代码将用户输入解读为度数。__

__Issue 4367↪https://gitlab\.com/gromacs/gromacs/\-/issues/4367__

##### 修复 : 前置因子为负时距离限制力的计算

##### 在计算距离限制力时，在力常数为负的情况下，弱限制违背的二次区和强限制违背的线性去互换了。

__Issue 4347↪https://gitlab\.com/gromacs/gromacs/\-/issues/4347__

##### GROMACS 2021\.5 发布注记

##### 该版本于 2022 年 1 月 14 日发布。这些发布注记记录了自上个2021\.4版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2020\.6版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

____Parrinello\-Rahman__ 压力耦合过程中不再缩放冻结原子的坐标__

__当使用Parrinello\-Rahman压力耦合时，盒子的缩放会应用于所有原子，从而导致冻结原子发生偏移。  
当模拟过程中压力发生显著变化时，这种效应对盒子两侧的影响更为剧烈。现在，冻结的原子会被压力  
耦合器忽略，具有冻结维度的原子会保持相应维度的坐标不变。__

__Issue 3075↪https://gitlab\.com/gromacs/gromacs/\-/issues/3075__

__使用 __FEP__ 运行 __AWH__ 时正确考虑来自 __PME__ 的 __DeltaH__ 贡献__

__当在GPU上或单独的PME进程上计算PME时，来自PME的线性dHdL贡献计算得太晚，以致没  
有考虑进AWH引导的FEP中。对于AWH引导的FEP的模拟结果，可以通过使用GPU或使用单独  
的PME进程计算PME，来验证所得的结果。__

__Issue 4294↪https://gitlab\.com/gromacs/gromacs/\-/issues/4294__

__修复 __AWH user PMF__ 读取大 __PMF__ 值的问题__

__在mdrun中读取用户提供AWH输入时，如果PMF的值大于88 kT，mdrun会退出并给出断言失败  
错误。现在，允许最大值为700 kT，超过这个值mdrun会退出，并给出明确的错误信息。__

__Issue 4299↪https://gitlab\.com/gromacs/gromacs/\-/issues/4299__

__gmx 工具的修复__

__gmx make\_edi 现在可以正确地关闭其输出文件__

##### 以前，该文件没有明确关闭，将结果留给了运行时环境。现在它可以在所有环境下都工作正常。

__修复 __gmx spatial__ 中的越界、溢出和不正确输出__

__gmx spatial内存管理中的几个问题都已经解决:__

__1\.越界的内存写入2\.当坐标正好处于边界上时，出现的令人困惑的错误信息（发生在使用\.xtc文件时）  
3\.由于整数溢出，归一化可能变成负数4\.负的\-ign\(默认\-1\)导致网格点的数目不正确5\.网格点的  
坐标不正确，特别是当\-ign不为零时6\.归一化计算不正确7\.默认的\-nab值从 4 增加到16\.__

__Issue 3214↪https://gitlab\.com/gromacs/gromacs/\-/issues/3214__

##### 影响便携性的修正

##### 杂项

__在 __Ampere__ 类 __Nvidia GPU__ 上运行时的性能改进__

##### 将短程非键内核的性能提高了12%\.

__Issue 3873↪https://gitlab\.com/gromacs/gromacs/\-/issues/3873__

##### GROMACS 2021\.4 发布注记

##### 该版本于 2021 年 11 月 5 日发布。这些发布说明记录了自上一个2021\.3版本以来GROMACS所发生

##### 的变化，以修复已知问题。它还纳入了2020\.6版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的描述。

__修复 __mdrun__ 可能表现不正确的地方__

##### 修复模拟带有虚拟位点的大体系时的崩溃

__当使用区域分解和OpenMP线程运行带有虚拟位点的大体系时，当一个区域及其邻域中的原子数超过  
200000 时，mdrun会崩溃。__

__Issue 4167↪https://gitlab\.com/gromacs/gromacs/\-/issues/4167__

##### 修复 GPU LINCS 偶尔向错误方向移动原子的问题

##### 由于CUDA版本的LINCS中缺少阻塞同步，共享内存偶尔会被新数据覆盖。这可能会略微影响移位后

##### 的原子的最终坐标。

__Issue 4199↪https://gitlab\.com/gromacs/gromacs/\-/issues/4199__

##### 禁止在 FEP 模拟中使用 PME 混合模式

__使用混合模式的PME（\-pme gpu \-pmefft cpu）会导致FEP模拟中计算的𝜕𝑉𝜕𝜆 不正确\.__

__只有在用户明确要求时才会使用混合模式\.__

__Issue 4190↪https://gitlab\.com/gromacs/gromacs/\-/issues/4190__

__修复当用其他维度运行 __FEP__ 时， __AWH__ 自由能输出中的虚假 __nan____

__当以炼金自由能微扰作为多个维度之一运行AWH时，由于日志操作失败，自由能输出可能包含nan。  
这并不影响AWH偏置，意味着模拟不受影响，但输出却受影响。__

__Issue 4180↪https://gitlab\.com/gromacs/gromacs/\-/issues/4180__

____mdrun__ 在没有 __MPI__ 的情况下也可以工作__

__当配置既不启用MPI，也不启用线程MPI时，mdrun会以断言失败而终止。__

__Issue 4264↪https://gitlab\.com/gromacs/gromacs/\-/issues/4264__

__修复 __gmx__ 工具__

__修复 __gmx convert\-tpr \-s \-o____

##### 以前，这个选项组合可以在提供索引文件的时候使用。现在这个组合在不提供索引文件时也可以基于默

##### 认索引组使用。

__当质心运动消除和位置约束联用时 __grompp__ 现在会再次给出注意提示__

__Issue 4128↪https://gitlab\.com/gromacs/gromacs/\-/issues/4128__

##### 大索引组的静态选择现在可以工作

__gmx distance \-f traj\.xtc \-n ndx\.ndx \-select "group "Contacts"" 这 样 的 命 令 只 有 在  
Contacts的大小小于原子数时才起作用。这个限制是一个错误，现在已经修复，因此Contacts可以具  
有任意大小。__

__基于索引组静态选区的其他类似使用现在也可以工作\.__

__Issue 4148↪https://gitlab\.com/gromacs/gromacs/\-/issues/4148__

##### 具有重复索引编号的索引组的静态选区现在可以工作

__在选区中引用索引文件的静态组（例如：gmx tool \-select "group \\"Contacts\\""\)只有当组内相邻__

__的索引编号不相同时才能正常工作。重复相同的索引编号可能是有意义的，例如在使用gmx distance__

__分析"1 2 2 3"的原子间距离时。以前，索引组必须写成"2 3 1 2"才能工作。__

__Issue 4149↪https://gitlab\.com/gromacs/gromacs/\-/issues/4149__

##### 影响可移植性的修复

##### 杂项

__修复一个影响重新运行 gmxapi 脚本的错误__

__一个拼写错误可能导致gmxapi模拟在中断后无法从检查点继续进行。这一错误在0\.2\.3版的gmxapi__

__Python包中得到了修正。__

__Issue 4267↪https://gitlab\.com/gromacs/gromacs/\-/issues/4267__

##### GROMACS 2021\.3 发布注记

##### 该版本于 2021 年 8 月 18 日发布。这些发布说明记录了自上一个2021\.2版本以来GROMACS所发生

__的变化，以修复已知问题。它还纳入了2020\.6版及以前的所有修正，你可以在 Release notes 发布注记中__

__找到这些修正的描述。__

__修复 mdrun 可能表现不正确的地方__

__修复 mdrun \-ddorder pp\_pme__

__当对PP\-PME进行进程排序时，mdrun在初始化阶段可能会出现死锁__

__Issue 4114↪https://gitlab\.com/gromacs/gromacs/\-/issues/4114__

__修正 gmxapi MD 插件绑定__

__当通过gmxapi Python接口添加到模拟中时，分子动力学扩展代码没有正确处理。这意味着在gmxapi  
版本>=0\.1时，会静默地取消限制势的施加。已经在gmxapi内部进行了更新。  
gmxapi 0\.2\.2 Python软件包支持更新的GROMACS API，如果模拟试图用兼容但已损坏的API  
（GROMACS 2021至2021\.2）来绑定外部插件代码，会产生错误。__

__第三方代码应该不需要更新，但开发者会注意到https://gitlab\.com/gromacs/gromacs/\-/tree/master/__

__python\_packaging/sample\_restraint（用于说明和测试目的）中额外的“null restraint”。__

__Issue 4078↪https://gitlab\.com/gromacs/gromacs/\-/issues/4078 and Issue 4102↪https://gitlab\.com/gromacs/gromacs/\-/issues/4102__

##### 430 第 7 章 发布注记

##### 修复从单进程模拟输出的的检查点重新启动多进程模拟的问题

##### 目前，单进程模拟从不使用更新组，但多进程运行可以这样做。这一修正确保了更新组中的原子总是从

##### 相同的周期性映像开始。以前，如果检查点是由单进程模拟输出的，无法保证这一点。

__Issue 4016↪https://gitlab\.com/gromacs/gromacs/\-/issues/4016__

__修复 __gmx__ 工具__

__修复 __gmx nmr \-viol__ 选项__

##### 该工具之前会以一个隐秘的错误失败。同时强制该选项与其他分析模式互斥。

__Issue 4060↪https://gitlab\.com/gromacs/gromacs/\-/issues/4060__

__修复 __gmx dipoles \-quad__ 选项__

##### 该工具现在可以报告正确的值\.

__Issue 4080↪https://gitlab\.com/gromacs/gromacs/\-/issues/4080__

__确保 __gmx convert\-tpr \-until__ 运行正常__

##### 在重构工具的内部结构时，这个选项被破坏了，不能正确计算剩余的步数。

__Issue 4056↪https://gitlab\.com/gromacs/gromacs/\-/issues/4056__

__修复 __gmx chi__ 和 __gmx angle__ 中的二面角转变计数__

##### 当使用只含 1 帧的轨迹时，不进行转变计数（以前会尝试进行并导致崩溃）。

##### 当使用含有多帧的轨迹时，转变计数是正确的（以前的不正确）。

__修复 __gmx chi__ 直方图中的可能崩溃__

##### 以前对残基名称使用了对临时字符串的无效引用，这可能会导致崩溃。

__修复 __gmx chi \-chi\_prod____

##### 以前，当相关二面角的数目与具有二面角的残基的数目不同时，它可能会崩溃或产生垃圾结果。

##### 7\.3\. GROMACS 2021 系列 \( 自此以下不再维护 \) 431

##### 影响可移植性的修复

__检查必要的 __python__ 模块是否可用__

##### 否则，源代码验证可能会导致构建失败，并出现隐秘错误。

__Issue 3985↪https://gitlab\.com/gromacs/gromacs/\-/issues/3985__

__确保 __NB\-LIB__ 和 __gmxapi__ 在没有启用测试的情况下也能构建__

##### 否则可能会导致隐秘的构建错误\.

##### 杂项

__移除 __mdrun__ 区域分解中的性能损失__

##### 在具有 16 或更多个所谓的PP MPI进程时，由于哈希表的大小不够理想，区域分解的重新划分可能会

##### 产生很大的性能开销。现在已经修复了。

__Issue 4054↪https://gitlab\.com/gromacs/gromacs/\-/issues/4054__

##### GROMACS 2021\.2 发布注记

##### 该版本于 2021 年 5 月 5 日发布。这些发布说明记录了自上一个2021\.1版本以来GROMACS所发生的

##### 变化，以修复已知问题。它还纳入了2020\.6版及以前的所有修复，你可以在发布说明中找到这些修复的

__说明。 Release notes 发布注记\.__

__修复 __mdrun__ 可能表现不正确的地方__

##### 移除了 GPU 更新可能出现的竞争条件

##### 修正了当使用GPU更新以及偶极矩计算时，坐标复制中可能出现的（但目前尚未观察到）竞争条件。

__Issue 4024↪https://gitlab\.com/gromacs/gromacs/\-/issues/4024__

__避免了 __md\-vv__ 中观察到的整体缩减问题__

__模块化模拟器中的md\-vv的新实现在从未使用过的非主进程上计算数值时可能会产生浮点异常。现在通  
过避免这种计算解决了这个问题。其他积分器不受影响，因为它们覆盖了计算所得的值。__

__Issue 4031↪https://gitlab\.com/gromacs/gromacs/\-/issues/4031__

##### 对具有微扰质量的原子禁止计算 SETTLE 相互作用

__较早的实现会产生不同程度的错误结果，因为这从未实现。现在mdrun和grompp都拒绝处理这样的体  
系，建议使用常规约束。__

__Issue 3959↪https://gitlab\.com/gromacs/gromacs/\-/issues/3959__

____Rerun__ 现在可以正确写下牵引模拟的输出__

__重构忽略了 pullf\.xvg和pullx\.xvg文件在重新运行期间应该输出。所有 2019 和 2020 的版本都受  
到影响，以及 2021 和2021\.1版本。现在，牵引输出文件的写入方式与 2018 及以前版本一样。__

__Issue 4043↪https://gitlab\.com/gromacs/gromacs/\-/issues/4043__

__修复 __gmx__ 工具__

__修复 __pdb2gmx__ 处理单残基链时的不正确行为__

##### 检查环形分子的代码可能导致单残基链被错误地视为环形分子。

__Issue 4029↪https://gitlab\.com/gromacs/gromacs/\-/issues/4029__

__修复 __grompp__ 对使用绝对参考的位置限制的检查__

__修复了grompp总是对位置限制给出关于使用绝对参考的警告，即使没有使用绝对参考也是如此。__

__Issue 3996↪https://gitlab\.com/gromacs/gromacs/\-/issues/3996__

##### 修复使用 VMD 插件时的错误

__工具会因C\+\+库的断言而崩溃，因为插件的加载代码错误地试图从nullptr构造一个字符串。__

__Issue 3055↪https://gitlab\.com/gromacs/gromacs/\-/issues/3055__

__修复 __gmx solvate__ 和 __gmx genion__ 的文件权限问题__

__这些工具以前写入临时文件时使用的Unix权限为 0600 。现在它们使用进程的umask（通常为 0644 ）。__

__Issue 4040↪https://gitlab\.com/gromacs/gromacs/\-/issues/4040__

##### 影响可移植性的修复

__支持 __Intel oneAPI__ 编译器 __2021\.2____

##### 修复了编译器数学和MKL的无穷大标志。

__修复 __Apple OpenCL__ 构建__

__Issue 4008↪https://gitlab\.com/gromacs/gromacs/\-/issues/4008__

##### 修复 GCC 11 的编译问题

__Issue 4039↪https://gitlab\.com/gromacs/gromacs/\-/issues/4039__

##### 杂项

##### 修复 GROMOS 力场中的键类型

##### \[ACE\]中C和\+N的键类型不正确。

__Issue 3995↪https://gitlab\.com/gromacs/gromacs/\-/issues/3995__

##### 允许 CPU 上的 PME 与区域分解和 GPU 更新一起运行

##### 放宽了一个限制，该限制禁止并行运行区域分解和GPU更新，并使用CPU进行PME（只要使用了组

##### 合的PP\-PME进程）。这使得在CPU资源足够用于PME时，并行运行可以扩展。

__Issue 4035↪https://gitlab\.com/gromacs/gromacs/\-/issues/4035__

##### GROMACS 2021\.1 发布注记

##### 该版本于 2021 年 3 月 8 日发布。这些发布说明记录了自上一个 2021 版本以来GROMACS所发生的变

##### 化，以修复已知问题。它还纳入了2020\.6版及以前的所有修正，你可以在发布注记中找到这些修正的说

##### 明。

__修复 __mdrun__ 可能表现不正确的地方__

__修复使用虚拟位点的 __MiMiC____

__看起来使用虚拟位点时MiMiC工作不正常，因为构建位点调用放在了使用位点的调用之后。现在应该  
工作正常了，但我们还没有测试是否如此。__

__Issue 3866↪https://gitlab\.com/gromacs/gromacs/\-/issues/3866__

__修复对 __dH/dlambda__ 的质量微扰__

__dH/dlambda中缺少质量微扰的贡献。请注意，用于Bennett接受率方法的外部能量差中并不缺少此贡  
献。__

__Issue 3943↪https://gitlab\.com/gromacs/gromacs/\-/issues/3943__

##### 使用卷积势和一个 FEP 维度运行 AWH 会得到错误结果

__当某个牵引维度使用awh\-potential = convolved并同时作为FEP维度时，输出的PMF是错误的。  
FEP维度始终使用伞形势，这种组合不能正常工作。已经在grompp中禁用了这种用法。__

__Issue 3946↪https://gitlab\.com/gromacs/gromacs/\-/issues/3946__

__移除 __md\-vv__ 中部分冻结的原子的速度__

__在约束过程中，md\-vv会在部分冻结的原子的冻结维度上添加一些速度。这并不会导致错误的轨迹，因  
为在传播过程中位置的冻结维度是固定的。然而，这些非零的速度会出现在轨迹和最终构型中。它们也  
可能导致计算的动能有些许错误，因为报告的动能是在速度限制后计算的。预期所有的影响都相对较小，  
因为它们不会累积，因为每一步的速度都会定期重置为零。__

__Issue 3849↪https://gitlab\.com/gromacs/gromacs/\-/issues/3849__

__修复 __gmx__ 工具__

##### 修复分析框架工具中的周期性边界条件

##### 轨迹分析框架中存在一个错误，会导致PBC下破碎的分子没有保持完整。这通常会导致分析输出中出

##### 现明显不正确的异常值。

__Issue 3900↪https://gitlab\.com/gromacs/gromacs/\-/issues/3900__

__修复 __gmx covar__ 中的范围检查错误__

__有一个检查颠倒了，导致使用了错误的范围检查。__

__Issue 3902↪https://gitlab\.com/gromacs/gromacs/\-/issues/3902__

__修复 __gmx xpm2ps__ 中的各种缺陷__

##### 自GROMACS 5\.1以来，在重构中引入了许多小问题，现已修复。

__Issue 3881↪https://gitlab\.com/gromacs/gromacs/\-/issues/3881__

##### 影响可移植性的修复

__修复 __Cygwin__ 上的编译__

##### 某个GROMACS头文件没有包含必要的标准头文件。此外，还解决了仅由POSIX定义而C\+\+未定

##### 义的M\_PI数学常数的问题。

__Issue 3890↪https://gitlab\.com/gromacs/gromacs/\-/issues/3890__

__改进了对 __FEP__ 维度采样时 __grompp__ 对 __AWH__ 设置的检查__

__确保在使用AWH对FEP维度进行采样时，AWH的采样间隔与nstcalcenergy 兼容。这可以避免  
AWH在采样的第一步（step>0）因设置不正确而导致崩溃。__

__Issue 3922↪https://gitlab\.com/gromacs/gromacs/\-/issues/3922__

##### 杂项

##### • 更新了GROMACS的标识

#### 7\.3\.2 主发布

##### 亮点

##### GROMACS 2021于 2021 年 1 月 28 日发布。此后可能会发布补丁，请使用更新后的版本\!以下是可以

##### 期待的一些亮点，更多细节见以下链接\!

##### 像往常一样，我们有一些有用的性能改进，无论是否使用GPU，都会默认启用和自动进行。此外，还有

##### 几个用于运行模拟的新功能。我们非常希望得到你的反馈，看看新版本在你的模拟和硬件上运行得如何。

##### 这些新功能包括：

##### • 支持多重时间步长，模拟速度接近翻倍，这旨在取代虚拟位点的处理方法

##### • 能够在平衡和成品模拟中使用随机晶胞重缩放压力控制方法

##### • 初步支持使用SYCL作为加速器框架

##### • 支持使用AWH进行自由能微扰

##### 436 第 7 章 发布注记

##### • 自由能模拟时支持将PME卸载到GPU

- __支持ARM SVE和富士通A64FX（Research Organization for Information Science and Technology  
（RIST）贡献）。__
- __NB\-LIB中新的非键相互作用API（与PRACE合作）。__
- __新的GROMACS标识\!__

##### 新特性和改进特性

##### 使用单个构建原子的虚拟位点

##### 可以在单个构建原子之上构建虚拟位点。这对于自由能计算有用。

##### 密度引导的模拟可以对结构应用矩阵乘法和移位矢量

__新的mdp选项 density\-guided\-simulation\-shift\-vector 可以定义一个移位矢量，在计算密度  
力之前，它可以移动密度引导的模拟组。有了可以使结构和输入密度对齐的已知移位矢量，这  
个功能可以使结构精修到非对齐的密度，而不需要对输入密度数据或结构进行处理。mdp选项  
density\-guided\-simulation\-transformation\-matrix可以定义一个矩阵，在应用移位矢量之前，这  
个矩阵可以与结构坐标相乘。这样可以对输入结构进行相对于输入密度的任意旋转、倾斜和缩放。一个  
典型的使用范例是嵌入膜的蛋白，不容易在膜内对它进行移位和旋转。__

##### 降低 SETTLE 导致的能量漂移

##### GROMACS已经对SETTLE中的质心计算进行了改进，以减少单精度模式下的能量漂移。现在，完全

__不进行质心计算，这大大减少了出现大的坐标值时的能量漂移。这样用SETTLE可以对尺寸达1000 nm  
的体系进行精确模拟（但要注意，用LINCS和SHAKE进行约束仍然会导致明显的漂移，这将体系尺  
寸限制在 100 到200 nm）。__

____mdrun__ 报告能量漂移__

__对于守恒积分器，mdrun现在会在日志文件中报告守恒能量的漂移。__

##### 使用 AWH 的 FEP

##### 现在可以使用加速权重直方图方法来控制自由能微扰模拟的状态。这可以作为多个AWH维度之一，

##### 同时其他维度与牵引坐标耦合。

____pdb2gmx__ 支持环状分子__

__现在可以在pdb2gmx中处理环状分子并为其生成GROMACS拓扑文件。__

##### 随机晶胞重缩放恒压器

##### 实现了随机晶胞重缩放恒压器。这是一个一阶、随机的压力控制方法，可以用于平衡和成品模拟。

##### 性能改进

##### 增加了对多重时间步进的支持

##### 实现了一种两级别的多重时间步进方案。可以选择五个不同的力索引组的任何组合来减少评估的频率，

##### 从而提高性能。

##### 扩展了对 GPU 版更新和约束的支持用例

##### GPU版的更新和约束现在可用于FEP，但不支持对质量和约束进行自由能微扰。

__减少 __grompp__ 在具有大量距离限制情况下的处理时间__

__gmx grompp处理距离限制的时间已经从正比于限制数目的二次方变为线性__

__Issue 3457↪https://gitlab\.com/gromacs/gromacs/\-/issues/3457__

##### S 支持在进行库仑 FEP 时将 PME 卸载到 GPU 上

##### 在进行库仑自由能微扰时，PME计算可以卸载到GPU上。

##### 简谐键的 CPU SIMD 加速实现

##### 键的SIMD加速略微提高了只含H键约束或没有约束的体系的性能。使用多重时间步进时，有显著改

##### 善。

##### 允许卸载 GPU 更新和约束，而不需要直接与 GPU 通信

##### 允许区域分解和单独的PME进程并行运行，以将更新和约束卸载到CUDA的GPU上，而（实验性

##### 的）不需要同时启用直接GPU通信功能。

__在 __NVIDIA Volta__ 和 __Ampere A100__ 上调整了 __CUDA__ 短程非键的内核参数__

__最近的编译器支持在NVIDIA Volta和Ampere A100 GPU上重新调整非键内核的默认值，从而提高了  
Ewald内核的性能，尤其是对那些也计算能量的内核。__

##### GROMACS 工具的改进

##### 错误修复

__修正了导出的 __libgromacs CMake__ 目标__

__更新导出的libgromacs CMake目标，使其不依赖于不存在的包含路径，并在接口定义中添加了  
GMX\_DOUBLE定义。该目标现在被导出到Gromacs命名空间。__

__Issue 3468↪https://gitlab\.com/gromacs/gromacs/\-/issues/3468__

__修正了 __pdb__ 文件中原子名称的非调用性更改__

__移除了读写pdb文件时更改原子名称的功能。这尤其会影响H原子的命名。__

__Issue 3469↪https://gitlab\.com/gromacs/gromacs/\-/issues/3469__

____pdb2gmx__ 更好地处理 __ASPH__ 和 __GLUH__ 输入__

##### 默认将所有这类残基视为非质子化形式，而不会尝试根据输入的残基名称推断质子化状态。质子化形式

__只能通过交互选择选项来实现。现在pdb2gmx在自动对这类输入残基进行转换时会报告。它还会确保  
输出构型和拓扑结构在默认和交互选择的情况下都能正确地命名此类残基。__

__Issue 2480↪https://gitlab\.com/gromacs/gromacs/\-/issues/2480__

##### 正确排除超出非键截断距离的微扰相互作用

##### 对于没有分子间相互作用耦合的自由能计算，可以排除距离超过截断距离的非键成对相互作用。这些相

##### 互作用仍会有PME长程贡献。现在，这些贡献都被移除了。此外，当存在超出配对列表截断距离的相

__互作用时，mdrun会推出并给出致命错误。__

__Issue 3403↪https://gitlab\.com/gromacs/gromacs/\-/issues/3403 Issue 3808↪https://gitlab\.com/gromacs/gromacs/\-/issues/3808__

##### 更正了 AWH 初始直方图大小

##### AWH偏差的初始直方图大小（微弱地）依赖于力常数。已经消除了这种依赖性，这使得直方图大小大

##### 致变为原来的 3 倍左右。实际中这对求解时间只有很小的影响。对于多个维度，会低估直方图的大小，

__特别是对存在慢速和快速维度组合的情况。现在参考手册中给出了初始直方图大小的简化公式。Issue__

__\(^3751\) ↪https://gitlab\.com/gromacs/gromacs/\-/issues/3751  
修复 __gmx xpm2ps__ 中刻度线间距的默认值__

##### 多年前，无意中改变了默认值，导致原定的自动刻度线间距的默认值被替换为一个不合适的固定值。

__Issue 3881↪https://gitlab\.com/gromacs/gromacs/\-/issues/3881__

__修正了使用截断静电时 __LJ Ewald__ 排除的问题__

__如果LJ Ewald与截断静电一起使用，那么CUDA和OpenCL内核中的排除力计算会出现错误。__

__Issue 3840↪https://gitlab\.com/gromacs/gromacs/\-/issues/3840__

__GROMACS的核心团队希望让用户和下游的开发者了解即将发生的变化，以便将干扰降到最低。如果你  
觉得有什么计划不合适，请与我们联系。__

__废弃的功能通常会在GROMACS中保留一年或更长时间，但不应再使用它们。__

##### GROMACS 2021 功能的预期变化

__gmx mdrun \-membed__

__将蛋白质嵌入膜的功能会保留，但可能采用不同的形式，如gmx membed\.__

__gmx mdrun \-rerun__

__从 轨 迹 计 算 势 能 量 的 功 能 会 保 留， 但 可 能 采 用 不 同 的 形 式， 如gmx rerun 和 gmx  
test\-particle\-insertion\.__

__积分器 __\.mdp__ 选项只包含动力学积分器__

__能量最小化会以不同的形式访问，也许是gmx minimize，并解读一个\.mdp字段以确定使用哪种最小化  
方法。简正模式分析可以使用gmx normal\-modes来进行。然后，这些工具的命令行帮助能够更好地记  
录哪些功能在什么时候被支持。__

__trjconv,editconf,eneconv 和 trjcat 中的许多功能__

##### 正在分离这些工具中的功能，以便能够在可组合的模块中使用它们，我们计划将其作为更简单的工具提

##### 供，并最终通过正在开发的GROMACS API提供。

__gmx do\_dssp 会被取代__

##### 这个工具被废弃了，因为对于一些用户来说，获取并安装一个单独的DSSP二进制文件存在问题，所以

__我们计划在某个时候使用一个原生的实现来取代它，可能会基于xssp，并使用一个新的gmx工具名称\.__

##### GROMACS 2021 中废弃的功能

__移除 __mdrun \-deffnm____

##### 当运行非常简单的模拟时，这个功能很方便，因为它会将一系列仅后缀不同的文件分组。然而，对于更

__一般的情况，当一个（或多个）mdrun模块写下多个\.xvg输出文件时，它无法工作，因为生成的文件名  
称会发生冲突。这一点，以及与检查点和追加的相互影响，导致了相当多的错误报告。__

__因为用户可以使用文件夹对文件进行分组（这是他们从GROMACS以外的经验中了解到的标准机制），  
如果移除mdrun \-deffnm这个曾经方便的选项，我们可以为用户构建和测试更好的软件。请相应地更新  
你的工作流程。__

__Issue 3818↪https://gitlab\.com/gromacs/gromacs/\-/issues/3818__

__作为 __GPU__ 框架的 __OpenCL__ 将被移除__

__Issue 3818↪https://gitlab\.com/gromacs/gromacs/\-/issues/3818 正在进行AMD和Intel GPU的移植工作，这些移植  
可能不会基于目前的GROMACS OpenCL端口。Nvidia GPU是CUDA端口的目标，预计不会有变化。  
在目前的资源水平下，核心团队无法维护、测试和扩展多达 4 种端口。由于没有看到HPC中新的GPU  
供应商需要OpenCL支持的前景，一旦AMD和Intel以其他方式提供支持，我们将移除OpenCL端口。__

____Intel KNC \(MIC\)__ 支持__

__Issue 3818↪https://gitlab\.com/gromacs/gromacs/\-/issues/3818这个架构在HPC中几乎已经绝迹了。请注意，对KNL  
的支持会继续下去，不受此废弃的影响。__

____Sparc64 HPC ACE____

__这个架构在HPC中几乎已经绝迹了。__

##### 遗留的 SIMD 架构支持

__Issue 3818↪https://gitlab\.com/gromacs/gromacs/\-/issues/3818 我们偶尔需要扩展GROMACS的SIMD框架，因此应  
该慢慢移除那些难以或无法测试的较旧架构。以下的实现已废弃，并且将来不会支持新的功能。__

- __Power 7__
- __ARMv7 \(该平台在GROMACS 2020中废弃\)__
- __x86 MIC \(该平台在GROMACS 2021中废弃\)__
- __Sparc64 HPC ACE \(该平台在GROMACS 2021中废弃\)__

__单纯构建 __GROMACS__ 的 __mdrun____

__Issue 3808↪https://gitlab\.com/gromacs/gromacs/\-/issues/3808 在构建GROMACS的封装二进制文件gmx之前，可  
以独立于许多其他默认的二进制工具进行构建mdrun二进制文件。在计算集群上安装时这很有用，因  
为mdrun的依赖性降到了最低。然而，我们现在用CMake可以更好地管理这些依赖关系，而且只构  
建mdrun的二进制文件也不再那么容易了。单纯mdrun的构建也更难测试，并且为GROMACS的文档  
编写，教用户使用带来了复杂性。因此，现在是移除该构建的时候了。__

__支持版本 __1__ 的硬件局部库 __hwloc____

__Issue 3818↪https://gitlab\.com/gromacs/gromacs/\-/issues/3818GROMACS已经支持版本 2 好几年了。GROMACS向  
前发展中最感兴趣的是较新硬件和硬件支持API的功能，所以我们应该尽量减少测试工作，鼓励集群升  
级旧的hwloc安装\.__

##### 遗留 API

__Issue 3818↪https://gitlab\.com/gromacs/gromacs/\-/issues/3818 遗留的安装头文件已废弃一段时间里，然而我们希望更  
广泛地指出，GROMACSsrc目录下的所有头文件都仅供内部使用，因此可能会更改而不另行通知。此  
外，libgromacs库的形式和内容以及相关的CMake目标可能会发生变化，因为我们正朝着建立能够长  
期稳定支持的API和支持机制的方向发展。__

##### 恒加速的 MD

__Issue 1354↪https://gitlab\.com/gromacs/gromacs/\-/issues/1354 这个问题已经存在很多年了，由于无人有兴趣修复，所  
以会移除。__

__gmx wham 读取 \.pdo 文件__

__在4\.0版之前，GROMACS的牵引代码会以\.pdo格式写下文件。对这种文件的分析可能已经没有意  
义，如果还有意义，使用任何更老的GROMACS版本都可以。如果我们不再支持读取\.pdo文件，gmx  
wham的维护和扩展会更加简单。__

##### 在 GROMACS 2020 中废弃的功能

##### 对 32 位架构的支持

__Issue 3252↪https://gitlab\.com/gromacs/gromacs/\-/issues/3252 目前没有使用 32 位架构的大规模机器，也没有相关的  
计划，我们也没有能力对其进行合适的测试和评估。__

##### 自由能软核幂 48

__Issue 3253↪https://gitlab\.com/gromacs/gromacs/\-/issues/3253 自由能软核幂 48 几乎从未使用过，因此已废弃。__

__对 __Armv7__ 的支持__

__Issue 2990↪https://gitlab\.com/gromacs/gromacs/\-/issues/2990 对于该架构当前代码存在一些问题，我们没有资源来支  
持和修复与之相关的问题。由于该架构对HPC的影响不大，因此被废弃。__

##### GROMACS 2019 废弃的功能

##### 生成虚拟位点以取代标准残基中的芳香环

__Issue 3254↪https://gitlab\.com/gromacs/gromacs/\-/issues/3254这些功能被认为在某些情况下会产生假象（未公布的结  
果），并且从未很好地测试过，也没有广泛使用，而且我们需要简化pdb2gmx\.__

__只有 __gmx benchmark__ 才支持基准测试选项__

__Issue 3255↪https://gitlab\.com/gromacs/gromacs/\-/issues/3255 诸如\-confout,\-resethway,\-resetstep等选项并未  
打算让普通mdrun用户使用，所以只让专用工具可以使用它们可能会更好。另外，这使得我们可以自定  
义默认值，例如在模拟的一部分结束时以适合所用mdrun和基准使用情况的方式写下文件，因此不再  
需要sphinxcode\-confout。__

__gmx mdrun \-nsteps__

__Issue 3256↪https://gitlab\.com/gromacs/gromacs/\-/issues/3256 \.tpr文件中的模拟步数可以使用gmx convert\-tpr来  
改变，或者在调用gmx grompp之前更改\.mdp文件中的值。这个mdrun选项提供了一定的便利性，但  
其实现的质量可疑、日志文件中也没有明确的记录，并缺乏维护。__

##### 移除的功能

##### 移除 GMX\_SCSIGMA\_MIN 环境变量

##### 这是用以重现4\.5之前GROMACS版本的自由能软核行为的。

##### 可移植性

__Python 环境__

__在需要Python的地方，支持CPython↪https://www\.python\.org3\.6到3\.8版本。__

__CMake现在使用 FindPython3↪https://cmake\.org/cmake/help/v3\.13/module/FindPython3\.html 来检测Python。如果你__

__以前使用PYTHON\_EXECUTABLE来提示Python解释器的位置，应该用CMake变量Python3\_ROOT\_DIR__

__或CMAKE\_PREFIX\_PATH来指定Python的”root”或”prefix”路径\(即包含\./bin/python3的目录\)。随__

__着其他基础设施的发展，PYTHON\_EXECUTABLE可能不再具有预期的作用，并不会给出警告。__

__CMake__

__将所需的CMake版本更新为3\.13。__

##### C\+\+ 标准

##### GROMACS将所需的C\+\+标准从C\+\+14更新为C\+\+17，并要求 2017 标准库的功能。详情见安装

##### 指南。

__Cygwin__

__GROMACS现在可以通过gcc和clang编译器在Cygwin上构建。__

__Windows__

__GROMACS现在可以在Windows上使用MSVC正确构建，即使源码或构建目录的路径中含有空格。__

__在CMake配置过程中，使用MSVC 2019进行的构建可以正确地检测到合适的静态链接设置。__

##### RDTSCP 的使用和报告

__现在GROMACS在x86上总是默认使用RDTSCP机器指令，以降低延迟时间。非常老的机器可能需  
要使用GMX\_USE\_RDTSCP=off进行配置。非x86平台不受影响，只是它们不会再报告RDTSCP被禁用  
（因为这是显然的）。__

__支持 __armv8\+sve \(ARM\_SVE\)____

__新增了对ARM Scalable Vector Extensions（SVE）的支持。GROMACS支持在CMake配置时固定  
SVE向量长度（通常通过\-msve\-vector\-bits= 编译器选项），GNU GCC 10及以后的版本都支  
持时发布，LLVM 12以及相关的编译器会很快支持。默认情况下，在CMake配置时检测默认的向量  
长度，可以用GMX\_SIMD\_ARM\_SVE\_LENGTH=选项来改变。支持的值为 128 、 256 、 512 和 1024 。请  
注意，还没有针对ARM\_SVE优化非键内核。ARM\_SVE支持由Research Organization for Science  
Information and Technology（RIST）贡献。__

##### 杂项

##### 温度和压力耦合间隔的默认值改为 10

__当nsttcouple 和nstpcouple 的默认mdp输入值为\-1 时，grompp会将这些值设置为nstlist。  
现在，这些默认值被设置为 10 ，因此与 nstlist无关（注意，grompp在需要精确积分时可能会选择  
更小的值）。__

__一致和手动的 __CMake GPU__ 支持配置__

__对CUDA和OpenCL的GPU加速设置已改为一致。现在可以通过在CMake配置中将GMX\_GPU设置  
为CUDA或OpenCL 来启用任一选项。为简化CMake代码，我们也放弃了基于构建主机自动选择选项  
的作法。特别是，这意味着除非明确启用GMX\_GPU选项，否则不会启用CUDA，而且CMake不会再执  
行尝试检测硬件，并在硬件可用时建议安装CUDA的额外步骤。除简化外，这也应该使得更容易处理  
多种不同的加速器API目标，例如NVIDIA硬件。__

__配置时的 __trivalue__ 选项从自动检测改为逻辑值开 __/__ 关__

__为简化CMake配置，避免出现用户直接控制之外的多种设置变化，我们取消了对自动设置逻辑值的支  
持。GMX\_BUILD\_HELP和GMX\_HWLOC现在默认禁用，而GMX\_LOAD\_PLUGINS默认启用。__

____gmxapi C\+\+__ 接口__

__gmxapi::Context 现在用gmxapi::createContext\(\)创建，允许客户端提供一个MPI通讯器给库使  
用，而不是使用其默认的通讯器（如MPI\_COMM\_WORLD）。支持MPI的客户端可以使用gmxapi/mpi/  
gmxapi\_mpi\.h模板头文件和assignResource\(\)辅助工具来生成createContext的参数。__

__统一几个 __CUDA__ 和 __OpenCL__ 的环境变量__

__统一了在OpenCL和CUDA中意义完全相同的环境变量：__

- __GMX\_CUDA\_NB\_ANA\_EWALD和GMX\_OCL\_NB\_ANA\_EWALD统一为GMX\_GPU\_NB\_ANA\_EWALD__
- __GMX\_CUDA\_NB\_TAB\_EWALD和GMX\_OCL\_NB\_TAB\_EWALD统一为GMX\_GPU\_NB\_TAB\_EWALD__
- __GMX\_CUDA\_NB\_EWALD\_TWINCUT 和 GMX\_OCL\_NB\_EWALD\_TWINCUT 统一为 GMX\_GPU\_NB\_EWALD\_\-  
TWINCUT__

##### 移除 QMMM 接口中不正常的部分

__目前，GROMACS只正式支持通过MiMiC的QM/MM；BioExcel正在开发新的CP2K QM/MM接  
口。所有其他的QM/MM支持都未经测试，而且很可能功能不全，现在已经从\.mdp输入和输出中移除  
了它们，这样grompp的\.mdp输出文件会更小。__

### 7\.4 GROMACS 2020 系列

#### 7\.4\.1 补丁发布

##### GROMACS 2020\.7 发布注记

##### 该版本于 2022 年 2 月 3 日发布。这些发布注记记录了自上个2020\.6版本以来GROMACS所发生的变

##### 化，以修复已知的问题。

__修复 __mdrun__ 可能表现不正确的地方__

##### 修复 : GPU LINCS 偶尔会使原子向错误方向移动

##### 由于CUDA版本的LINCS中缺少阻塞同步，新数据偶尔会覆盖共享内存。可能会稍微影响被移动原子

##### 的最终坐标。

__Issue 4199↪https://gitlab\.com/gromacs/gromacs/\-/issues/4199__

##### 修复 : 大限制偏差的限制势计算

##### 代码中的计算并未遵循手册中的势能说明，但电势以二次方持续增长，而不是以应有的线性增长。

__Issue 4346↪https://gitlab\.com/gromacs/gromacs/\-/issues/4346__

__修复 __gmx__ 工具__

##### 影响可移植性的修复

##### 杂项

##### GROMACS 2020\.6 发布注记

##### 该版本于 2021 年 3 月 4 日发布。这些发布注记记录了自上个2020\.5版本以来GROMACS所发生的变

##### 化，以修复已知的问题。

__修复 __mdrun__ 可能表现不正确的地方__

__余弦加速如果无法运行则无法中止__

__余弦加速仅与蛙跳式积分器\(integrator = md\)兼容。然而，GROMACS确实接受使用其他积分算法  
进行余弦加速的输入文件，并报告这些模拟中与粘度有关的量。由于余弦加速从未用于这些情况，因此  
任何模拟如果启用了余弦加速,并使用了md以外的积分器,所得结果都应被视为无效。__

__Issue 3903↪https://gitlab\.com/gromacs/gromacs/\-/issues/3903__

__修复 __gmx__ 工具__

__修复 __: gmx covar__ 中的范围检查错误__

##### 检查被反转，导致所用范围检查错误。

__Issue 3902↪https://gitlab\.com/gromacs/gromacs/\-/issues/3902__

##### 影响可移植性的修复

##### 杂项

##### GROMACS 2020\.5 发布注记

##### 该版本于 2021 年 1 月 6 日发布。这些发布注记记录了自上个2020\.4版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2019\.6版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

__修复 __mdrun__ 可能表现不正确的地方__

__修复 __: mdrun__ 在检查点之前写出零 __dH/dlambda__ 和外部 __lambda__ 能量__

__运行自由能计算时，若separate\-dhdl\-file=no且nstdhdl不是nstenergy的倍数，对最后一个能量帧和  
检查点之间的步骤, mdrun会将零值的dH/dlambda和外部能量写入能量文件。这会导致自由能估计出  
现错误，而这些错误可能会被忽视，因为值只在几步中有偏差。__

__Issue 3763↪https://gitlab\.com/gromacs/gromacs/\-/issues/3763__

##### 修复 : 使用区域分解的 COM 牵引 , 具有权重或 >32 进程

##### 同时使用COM牵引和区域分解时，如果使用每个原子的相对权重,或使用超过 32 个DD MPI进程，

##### 结果不正确。这通常会导致崩溃或明显错误的结果。

__Issue 3750↪https://gitlab\.com/gromacs/gromacs/\-/issues/3750__

##### 修复 : 多个步进器共享偏置时 AWH 自由能不正确

##### 当多个步进器共享AWH偏置时，AWH自由能输出不正确。误差随着自由能更新间隔以及步进器数目

##### 的二次方上升。随着更新大小随着时间的推移而减小，误差也会减小。这意味着使用默认AWH设置时，

__误差可以忽略不计。在自由能更新间隔为2 ps的情况下，对于相当快的反应坐标,我们观察到的误差大  
约等于使用 32 个步进器的统计误差。对于较慢的坐标，误差将小于统计误差。__

__Issue 3828↪https://gitlab\.com/gromacs/gromacs/\-/issues/3828__

##### 修复 : MTTK 的守恒能量

__当使用pcoupl=MTTK和tcoupl=nose\-hoover时，计算的守恒能量不正确，因为存在两个错误,可分别  
追溯到GROMACS 4\.6和 2018 。因此，自GROMACS 4\.6以来的任何GROMACS版本中,使用这种温  
度和压力耦合算法组合时,所有报告的守恒能量都可能是错误的。注意，这些误差不会影响动力学，因  
为只会报告守恒能量，但从未在计算中使用它。另请注意，此错误仅影响这种温度/压力耦合算法的精确  
组合。__

__Issue 3796↪https://gitlab\.com/gromacs/gromacs/\-/issues/3796__

__修复 __: Nose\-Hoover__ 的守恒能量__

__当使用tcoupl=nose\-hoover,且一个或多个温度组具有非整数自由度时，计算的守恒能量不正确,错误  
可追溯到GROMACS 2018。自GROMACS 2018以来的,若使用Nose\-Hoover温度耦合和非整数自由  
度\.报告的守恒能量可能会略有下降。注意，这些误差不会影响动力学，因为只会报告守恒能量，但从未  
在计算中使用它。另请注意，只有在使用小的温度组或小型体系时，错误才明显。__

__Issue 3831↪https://gitlab\.com/gromacs/gromacs/\-/issues/3831__

##### 修复 : MTTK 的动能和温度报告

__当使用pcoupl=MTTK和tcoupl=nose\-hoover，报告的动能和温度略有偏差。温度耦合积分落后于报告  
半个时间步长。请注意，这些错误不会影响动力学，因为对相关量的积分正确，只是报告出现错误。另  
请注意，差异非常小，以致于除严格的算法验证之外，对任何应用来说都不可能产生显著影响。最后，  
请注意，此错误仅影响这种温度/压力耦合算法的精确组合。__

__Issue 3832↪https://gitlab\.com/gromacs/gromacs/\-/issues/3832__

##### 修复 : 角度和二 面角的牵引错误消息

__当mdrun退出时，COM牵引代码可能会打印不正确的牵引组索引，并出现有关角度和二面角几何中牵  
引距离太长的错误。__

__Issue 3613↪https://gitlab\.com/gromacs/gromacs/\-/issues/3613__

##### 修复 : 扩展系综中的数值问题

##### 当执行模拟回火或扩展系综模拟时，若哈密顿量的变化太大，那么蒙特卡罗会建议不太可能会下溢的状

##### 态，导致除以零错误。通过数值强化逻辑流程解决了这个问题，这样就会拒绝这些建议。

__Issue 3304↪https://gitlab\.com/gromacs/gromacs/\-/issues/3304__

##### 修复 : 施加电场的电场强度不正确

##### 当与区域分解一起使用时，电场模块生成的电场不正确，因为错误地将场索引用于所有原子而不是仅用

##### 于当前区域上的原子。

##### 对于区域之间的重叠区域，其厚度为配对列表截断距离，电场会加倍（对2D或3D区域分解会更大）。

##### 为验证该问题是否会影响模拟，用户应使用泊松方程计算跨过模拟盒子的实际势能。如果该势能与作为

##### 输入提供的势能一致，则模拟不会受到影响。

__Issue 3800↪https://gitlab\.com/gromacs/gromacs/\-/issues/3800__

__修复 __gmx__ 工具__

__改进 __gmx do\_dssp__ 中的 __CHARMM__ 支持__

__Issue 3568↪https://gitlab\.com/gromacs/gromacs/\-/issues/3568__

__修复不起作用的 __gmx h2order \-d__ 选项__

__gmx h2order工具始终采用沿z轴的法向。__

__Issue 3820↪https://gitlab\.com/gromacs/gromacs/\-/issues/3820__

##### 修复牵引组索引处理

__牵引代码没有正确地验证其索引组，从而导致grompp时无限循环或触发断言。__

__Issue 3810↪https://gitlab\.com/gromacs/gromacs/\-/issues/3810__

##### 影响可移植性的修复

##### 修复 OSX 上的构建

__由于缺少include，该代码无法编译。__

__Issue 3730↪https://gitlab\.com/gromacs/gromacs/\-/issues/3730__

##### 杂项

##### GROMACS 2020\.4 发布注记

##### 该版本于 2020 年 10 月 6 日发布。这些发布注记记录了自上个2020\.3版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2019\.6版及以前的所有修正，你可以在发布注记中找到这些修正

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

##### 修复 : GPU 版本的 LINCS 在多区域情况下的错误

##### 增加区域中耦合约束的最大数目不会触发内存重新分配，现已修复。例如，当大的分子进入先前被较小

##### 分子占据的区域时，就会发生这种情况。该错误不影响单个区域的情况。

##### 修复 : 区域分解时 N 体虚拟位点的索引处理

##### 区域分解代码中处理N体虚拟位点时使用了不正确的索引。这通常会因非法或不正确的内存使用而导致

##### 崩溃。

__Issue 3635↪https://gitlab\.com/gromacs/gromacs/\-/issues/3635__

##### 修复 : 使用 LJ\-PME 和色散校正时断言失败

__使用vdw\-type=PME和色散校正时，mdrun会在PME调整期间因断言失败而退出。__

__Issue 3677↪https://gitlab\.com/gromacs/gromacs/\-/issues/3677__

##### 修复 : 使用模块化模拟器和区域分解时 FEP 计算错误

__当使用模块化模拟器、区域分解进行质量微扰的自由能计算时，会始终使用lambda=0处的质量而不是__

__实际的lambda值时的质量来执行模拟。__

__添加了 Ryzen 上 RDRAND 并不总是返回随机数的解决方法__

__在AMD Ryzen 3000系列CPU上，硬件随机数生成器\(RDRAND\)可能表现不正确，始终返回\-1  
\(0xFFFFFFFF\)。当运行时检测到此硬件错误时，GROMACS会切换到基于软件的伪随机数生成器。  
虽然许多主板供应商一直在分发包含微代码修复的固件更新，并且大多数主板在出厂时已安装了这些固  
件更新，但仍然可能有一些系统未收到更新而受到影响。  
如果你在这些系统上运行模拟，理论上所有随机数种子都可能受到影响（请参阅下面的算法），因为这  
意味着使用相同的种子。即使这对于几乎所有的单独模拟来说都应该没问题，因为生成的数字仍然是随  
机的。最有可能受到严重影响的情况是，如果你使用相同的起始构型,并使用自动生成的不同随机种子  
（而不是手动选择种子）开始许多模拟\-那么Ryzen硬件错误可能意味着你的所有模拟实际上都会具有  
相同的初始速度或相同的随机变化等，具体取决于你使用的算法。  
受影响的算法列表如下：  
1\.如果没有使用用户提供的种子（例如，如果使用\-1 要求GROMACS生成种子），则gmx grompp  
中的种子会受到影响。这可能会影响朗之万/随机动力学、速度重缩放恒温器、任何与蒙特卡洛相  
关的,以及随机速度的生成。  
2\.在副本交换模拟过程中决定何时交换副本。  
3\.使用来自AWH的随机分量进行的模拟。  
4\.一些分析和准备工具可能会受到影响，例如自由体积计算、离子放置、WHAM、简正模式分析和  
PME误差估计。  
诊断：为帮助检测错误，请使用GROMACS 2020\.4或更高版本运行gmx mdrun \-debug 1，然后会生  
成调试日志，通常称为gmx\.debug\.如果程序运行的处理器受到影响，此文件会包含以下消息：__

- __Hardware random number generator \(RDRAND\) returned \-1 \(0xFFFFFFFF\) twice in a row\. This  
may be due to a known bug in AMD Ryzen microcode\. Will use pseudo\-random number generator  
\(PRNG\) rather than hardware device\.  
硬件随机数生成器\(RDRAND\)连续两次返回\-1 \(0xFFFFFFFF\)。这可能是由于AMD Ryzen微  
代码中的一个已知错误造成的。将使用伪随机数生成器（PRNG）而不是硬件设备。  
在受影响系统上,早期发布将无法通过单元测试套件中的SeedTest\.makeRandomSeed测试。要进行检  
查，请在构建文件夹中运行make check。你还可以在下面的链接中找到示例测试代码。  
有 关 该 问 题 的 更 多 信 息， 请 查 看 此 网 站↪https://arstechnica\.com/gadgets/2019/10/  
how\-a\-months\-old\-amd\-microcode\-bug\-destroyed\-my\-weekend/\.__

__修复 __gmx__ 工具__

__修复 __: gmx trjcat \-demux__ 的默认输出__

##### 使用默认文件名输出时不会写入文件。

__Issue 3653↪https://gitlab\.com/gromacs/gromacs/\-/issues/3653__

##### 影响可移植性的修复

##### 支持 CUDA 11\.0

##### 使用CUDA 11\.0的构建现在可以配置并通过了测试。使用CUDA 11\.0构建意味着不再支持CC 3\.0的

##### 硬件，现在可以使用CC 8\.0。

__Issue 3632↪https://gitlab\.com/gromacs/gromacs/\-/issues/3632__

##### 修复 : 使用 MSVC 构建

##### 由于缺少标题行，构建会失败。

__Issue 3669↪https://gitlab\.com/gromacs/gromacs/\-/issues/3669__

__仅在 __x86__ 平台上检查 __RDTSCP____

##### 杂项

__修复 __:__ 整个冻结时 __grompp__ 崩溃__

__When the whole system would be frozen, grompp would crash with a segmentation fault\.当冻结整个体  
系时，grompp会因段错误而崩溃。__

__Issue 3683↪https://gitlab\.com/gromacs/gromacs/\-/issues/3683__

##### 修复 : 模拟后是输出中分子索引的意外变化

##### 重复分子的分子索引现在重新按预期连续编号（而不是全部为 1 ）。

__Issue 3575↪https://gitlab\.com/gromacs/gromacs/\-/issues/3575__

__修复 __: libgromacsCMake__ 目标的 __INTERFACE\_INCLUDE\_DIRECTORIES____

__libgromacs\.cmake格式错误，引用了不存在的目录。__

__Issue 3592↪https://gitlab\.com/gromacs/gromacs/\-/issues/3592__

##### GROMACS 2020\.3 发布注记

##### 该版本于 2020 年 7 月 9 日发布。这些发布注记记录了自上个2020\.2版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2019\.6版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

__修复 __mdrun__ 可能表现不正确的地方__

__修复 __gmx__ 工具__

__修复 __:__ 某些较旧 __tpr__ 文件读取错误__

__某些较旧的tpr文件可能会被错误读取，通常会导致退出并出现内存分配错误。__

__修复 __: gmx lie__ 段错误__

__由于文件中能量项的尺寸与F\_NRE不匹配，该工具会崩溃。__

__Issue 3547↪https://gitlab\.com/gromacs/gromacs/\-/issues/3547__

__修复 __: gmx xpm2ps__ 的矩阵读取__

##### 如果没有提供第二个矩阵，该工具将无法读取矩阵。

__Issue 3551↪https://gitlab\.com/gromacs/gromacs/\-/issues/3551__

__修复 __: gmx hbond__ 中的未初始化变量警告__

##### 由于使用未初始化的内存，工具会产生垃圾。

__Issue 3550↪https://gitlab\.com/gromacs/gromacs/\-/issues/3550__

__修复 __:__ 再次修复 __gmx do\_dssp____

__在上次修复后，该工具仍然损坏并给出错误结果。__

__Issue 3444↪https://gitlab\.com/gromacs/gromacs/\-/issues/3444__

__允许配置 __dssp__ 的默认路径__

__用户可以使用GMX\_DSSP\_PROGRAM\_PATH配置dssp的默认路径。__

__Issue 3520↪https://gitlab\.com/gromacs/gromacs/\-/issues/3520__

__避免 __gmx genrestr__ 中的段错误__

##### 由于访问已释放内存而导致内存访问错误，该工具在运行简单输入时可能会失败。

__Issue 3582↪https://gitlab\.com/gromacs/gromacs/\-/issues/3582__

##### 影响可移植性的修复

##### 更新 MSVC SIMD 标志

__新支持的SIMD标志可能会提高运行Windows的最新x86的性能。__

__修复 __tinyxml2__ 链接错误__

##### 链接外部库的签名不正确。

##### 杂项

##### 更新了有关 GPU 上使用非动力学积分器的消息

##### PME和成键力的GPU实现需要动力学积分器。告知用户为什么使用GPU进行PME或成键力计算时

##### 不支持非动力学积分器的消息现在更加清晰。

##### GROMACS 2020\.2 发布注记

##### 该版本于 2020 年 4 月 30 日发布。这些发布注记记录了自上个2020\.1版本以来GROMACS所发生的

##### 变化，以修复已知的问题。它还纳入了2019\.6版及以前的所有修复，你可以在发布注记中找到这些修复

##### 的说明。

__修复 __mdrun__ 可能表现不正确的地方__

____Ewald__ 偶极子校正在没有区域分解的情况下不正确__

__当不使用区域分解时，现在禁用Ewald偶极校正\(epsilon\-surface \!= 0\)。使用区域分解时，它仅当每个  
分子由单个更新组组成时（例如水）才起作用。这将在 2021 发布中修复。__

__Issue 3441↪https://gitlab\.com/gromacs/gromacs/\-/issues/3441__

##### 从检查点重新启动扩展系综模拟

__当从检查点重新启动扩展系综模拟时，扩展系综会默默地拒绝运行，并且模拟保持其原始lambda状态。__

__Issue 3465↪https://gitlab\.com/gromacs/gromacs/\-/issues/3465__

##### 修复 : 使用 LJ PME 时的自由能计算

__修复了使用自由能微扰且vdwtype = pme时长程校正错误的问题。这影响了力、能量、lambda导数和  
外部lambda。__

__Issue 3470↪https://gitlab\.com/gromacs/gromacs/\-/issues/3470__

__现在，使用 __\-update gpu__ 时，可以正确移除质心速度__

##### 当移除质心运动时，会在CPU内存中更新速度。对GPU更新的情况，则应在CPU上更新后将速度复

##### 制回GPU内存。这会影响大多数必须移除质心速度的模拟，特别是那些运行开始时速度较大的模拟。

__Issue 3508↪https://gitlab\.com/gromacs/gromacs/\-/issues/3508__

##### 修复 : 以非零初始步数重新启动检查点

__从检查点重新启动时，在检查模拟是否已完成时会忽略init\-step mdp参数。因此，只有当init\-step为  
0 或未指定时，此检查才工作正常。__

__Issue 3489↪https://gitlab\.com/gromacs/gromacs/\-/issues/3489__

__修复 __gmx__ 工具__

__时间输出单位修复__

__当选择微秒或更大的时间单位时，gmx tool \-tu现在会在\.xvg特别是\.xvgr绘图中生成正确的字符串\.__

__修复 __do\_dssp____

##### 该工具出现段错误。

__Issue 3444↪https://gitlab\.com/gromacs/gromacs/\-/issues/3444__

##### 影响可移植性的修复

__提供有关在 __gcc > 9__ 中不检测 __IBM\_VSX__ 支持的清晰的消息__

__CMake会失败并给出令人困惑的错误消息。__

__Issue 3380↪https://gitlab\.com/gromacs/gromacs/\-/issues/3380__

##### 杂项

##### 修复了初始 DLB 状态报告

__当mdrun启动时若选择“on”或“auto”值，日志文件中会错误地报告初始DLB状态。__

##### GROMACS 2020\.1 发布注记

##### 该版本于 2020 年 3 月 3 日发布。这些发布注记记录了自上个 2020 版本以来GROMACS所发生的变

##### 化，以修复已知的问题。它还纳入了2019\.6版及以前的所有修正，你可以在发布注记中找到这些修正的

##### 说明。

__修复 __mdrun__ 可能表现不正确的地方__

__修复 __:__ 使用 __mdrun \-multidir__ 时若每个模拟超过一个进程出现致命错误__

__Issue 3296↪https://gitlab\.com/gromacs/gromacs/\-/issues/3296__

__修复 __:__ 使用多个进程和单独的 __PME__ 进程时 __mdrun__ 会出现死锁__

__当使用多个PP进程以及单独的PME进程时，mdrun可能会在开始PP\-PME均衡之前陷入死锁。__

__Issue 3335↪https://gitlab\.com/gromacs/gromacs/\-/issues/3335__

__使用 __shell__ 运行并在 __GPU__ 上更新时避免 __mdrun__ 断言失败__

__mdrun任务分配代码中添加了对shell的检查，以便mdrun在尝试使用shell运行并在GPU上更新时  
回退到CPU或给出明确的错误消息。__

__Issue 3303↪https://gitlab\.com/gromacs/gromacs/\-/issues/3303__

____mdrun MPI__ 进程计数时允许使用大的质数因子__

##### 即使用户指定了网格，区域分解也会拒绝运行时在MPI进程计数中使用大的质数因子。

__Issue 3336↪https://gitlab\.com/gromacs/gromacs/\-/issues/3336__

__实际修复自由能计算但不微扰 __q/LJ__ 时 __PME__ 力的计算__

##### 若实际上没有对电荷或LJ原子类型进行微扰，PME会错误地忽略微扰原子上的网格力。请注意，这是

##### 一种相当罕见的情况。

__Issue 2640↪https://gitlab\.com/gromacs/gromacs/\-/issues/2640 Issue 3359↪https://gitlab\.com/gromacs/gromacs/\-/issues/3359__

##### 检查缺失的 DD 相互作用时避免死锁

__当检测到区域分解后缺失成键相互作用时，mdrun会死锁，而不是失败退出。__

__Issue 3373↪https://gitlab\.com/gromacs/gromacs/\-/issues/3373__

__修复 __:__ 检查点重新启动时使用 __Parrinello\-Rahman__ 和 __md\-vv____

__使用Parrinello\-Rahman和md\-vv（仅在新的模块化模拟器方法中实现）的检查点文件无法读取。__

__Issue 3377↪https://gitlab\.com/gromacs/gromacs/\-/issues/3377__

##### 避免程序在使用取向限制时频繁中止

__mdrun可能会在检查多个分子中的取向限制时中止，即使没有对它们施加限制。__

__Issue 3375↪https://gitlab\.com/gromacs/gromacs/\-/issues/3375__

__当模拟共享状态在不同步数开始时，为 __mdrun \-multidir__ 添加致命错误__

__当（重新）启动mdrun \-multidir进行共享状态数据的模拟（例如，副本交换、共享偏置的AWH或  
NMR系综平均）时，若初始步数不同只会打印注释，这可能导致模拟不同步。现在对这种情况会发出  
致命错误。__

__Issue 2440↪https://gitlab\.com/gromacs/gromacs/\-/issues/2440 Issue 3990↪https://gitlab\.com/gromacs/gromacs/\-/issues/3990__

##### 使用模块化模拟器且没有 DD 时 , 检查斜盒子是否正确

##### 使用不带DD的模块化模拟器，使用压力控制时无法检查盒子是否过度倾斜。

__Issue 3383↪https://gitlab\.com/gromacs/gromacs/\-/issues/3383__

##### 修复 : 使用模块化模拟器的 NMR 限制

##### 在模块化模拟器下NMR限制（距离或取向限制）未按预期工作。所有取向限制模拟都会因段错误而失

##### 败，使用时间平均的距离限制模拟也是如此。所有其他距离限制模拟都可以正确运行，但只有在与一般

##### 能量写入步骤一致时才会输出到能量轨迹。

__Issue 3388↪https://gitlab\.com/gromacs/gromacs/\-/issues/3388__

##### 使用色散校正时避免整数溢出

##### 更改了存储索引的整数类型,意味着值可能会溢出并变为负数，从而导致错误的查找和无意义的值。

__Issue 3391↪https://gitlab\.com/gromacs/gromacs/\-/issues/3391__

__修复 __: Intel GPU__ 上过小的配对列表缓冲__

__为Intel GPU生成的配对列表缓冲区稍微太小，因为假定使用4x4原子簇对内核而不是4x2。__

__Issue 3407↪https://gitlab\.com/gromacs/gromacs/\-/issues/3407__

##### 修复 : 检查点文件与共享数据的模拟不同步

##### 当模拟共享数据时，例如副本交换、共享偏置的AWH或NMR系综平均，现在已在重命名检查点文件

##### 之前添加了MPI屏障，以避免模拟中的检查点文件不同步。现在，只有在极不可能的情况下，某些检查

##### 点文件可能具有临时名称，但所有内容都会同步。

__Issue 2440↪https://gitlab\.com/gromacs/gromacs/\-/issues/2440__

##### 修复 : 使用图形和模块化模拟进行的模拟

##### 使用模块化模拟器和图形对象进行的模拟会因段错误而失败。

__Issue 3389↪https://gitlab\.com/gromacs/gromacs/\-/issues/3389__

##### 修复 : 使用冻结原子时质心运动的移除

##### 当冻结原子是质心运动移除组的一部分时，它们仍会对这些组的质量做出贡献。这意味着COM速度修

__正（稍微）太小。现在，grompp会从COM移除组中移除完全冻结的原子。当原子仅沿一维或二维冻  
结且属于COM移除组的一部分时，grompp现在会发出警告。__

__Issue 2553↪https://gitlab\.com/gromacs/gromacs/\-/issues/2553__

##### 修复 : 移除部分体系的质心运动时的温度计算

##### 在不常见的情况下，会移除体系一部分而不是整个体系的质心运动，未移除质心运动的那部分的自由度

##### 数将错误地降低为1/3。

__Issue 3406↪https://gitlab\.com/gromacs/gromacs/\-/issues/3406__

##### 修复 : 选择未定义的 NB 内核类型时可能出现的问题

##### NB内核的CPU参考实现对特定内核类型缺少一些定义。这仅影响明确关闭SIMD的安装，这在生产

##### 环境中不太可能发生。

__Issue 2728↪https://gitlab\.com/gromacs/gromacs/\-/issues/2728__

__修复 __gmx__ 工具__

##### 影响可移植性的修复

__添加对 __ICC NextGen__ 的支持__

__添加对基于LLVM技术的Intel编译器的支持。要使用此编译器编译GROMACS，请使用CXX=icpc  
CXXFLAGS=\-qnextgen cmake\.__

__记录 __Volta__ 和 __Turing__ 上 __OpenCL__ 的已知问题__

__Issue 3125↪https://gitlab\.com/gromacs/gromacs/\-/issues/3125__

##### 杂项

##### 修复 : 发布压缩包中对已修改源文件的检查

##### 如果在生成构建目录之后对源码进行了修改，则可能不会获知这些修改。

__Issue 3302↪https://gitlab\.com/gromacs/gromacs/\-/issues/3302__

#### 7\.4\.2 主发布

##### 亮点

##### GROMACS 2020于 2020 年 2 月 1 日发布，此后可能会有补丁发布，请使用更新的版本\!以下是你可以

##### 期待的一些亮点，相应链接中的有更多细节\!

##### 像往常一样，我们有一些有用的性能改进，无论是否有GPU，都会默认自动启用。此外，还有用于运行

##### 模拟的几个新功能。我们极其希望得到您的反馈，看看新发布在您的模拟和硬件上运行情况如何。这些

##### 新功能包括：

##### • 密度导向模拟允许将原子“拟合”到三维密度图。

- __包含gmxapi 0\.1，这是一个API和用户接口,用于管理复杂模拟、数据流和即插式分子动力学扩  
展代码。__
- __新的模块化模拟器,它可以根据描述每个模拟步骤中发生的不同计算的单个对象进行构建。__
- __Parrinello\-Rahman压力耦合器现在也可用于md\-vv积分器。__
- __对支持的模拟类型,可以在单个CUDA兼容GPU上运行几乎整个模拟步骤，包括坐标更新和约  
束计算。__

##### 新特性和改进特性

##### 密度导向模拟

##### 用户现在可以施加来自三维参考密度的额外力。通过增加模拟密度与参考密度的相似性，这些力可以将

##### 原子“拟合”到密度中。

##### 有多种方案可用于计算模拟密度以及评估参考密度和模拟密度之间的相似性。

##### 位于两原子连线上且距离固定的虚拟位点

##### 这可用于某些情况,如CHARMM力场中的卤素。

__Issue 2451↪https://gitlab\.com/gromacs/gromacs/\-/issues/2451__

____gmxapi Python__ 支持__

__当用户安装 gmxapi Python包时，在默认GROMACS安装中,可以使用Python进行数据流驱动的模  
拟和分析。请参阅 gmxapi Python 包。__

##### 新的模块化模拟器

##### 引入了一种如何在单个模拟步骤中组合各个计算步骤的新方法，重点关注可扩展性和模块化。该模拟器

__现在是在NVE、NVT（仅限v\-rescale恒温器）、NPT（仅限v\-rescale恒温器和Parrinello\-Rahman恒  
压器）或NPH（仅限Parrinello\-Rahman恒压器）中使用速度Verlet进行模拟时的默认模拟器，进行  
或不进行自由能微扰都可以。__

##### 性能改进

##### 非键自由能内核加速比高达 2\.5

##### 非键自由能内核在非零A和B状态下的加速比为2\.5，在零状态下为1\.5。当非微扰的非键计算卸载到

##### GPU时，尤其可以提高运行性能。在这种情况下，PME网格计算现在总是占用最多的CPU时间。

##### 傅里叶类型的正常二面角和周期类型的反常二面角支持 SIMD 加速

__当 __GROMACS__ 不使用 __AVX512__ 时，避免配置启用 __AVX512__ 的 __own\-FFTW____

##### 以前，如果配置GROMACS可以使用任何AVX，则内部构建的FFTW会配置为也包含AVX512内核。

##### 如果（通常很烦人）FFTW自动微调器在运行中选择AVX512内核，而该内核仅使用AVX/AVX2,并

##### 可以在更高的CPU时钟下运行，而不受AVX512时钟速度限制，则可能会导致性能损失。现在，如果

##### GROMACS也配置了相同的SIMD，则AVX512仅用于内部FFTW。

##### 更新和约束可以在 GPU 上运行

##### 对于标准模拟（请参阅用户指南了解更多详细信息），可以使用CUDA将更新和约束都卸载到GPU。因

##### 此，模拟中所有计算密集的部分都可以卸载，在使用快速GPU和慢速CPU情况下这样做性能更好。默

__认情况下，更新会在CPU上运行，要在单进程模拟中使用GPU，可以使用新的‘\-update gpu’命令行  
选项。对于区域分解的使用，请参见下文。__

##### GPU 直接通信

##### 当使用CUDA在多个GPU上运行时，现在可以直接在GPU内存空间之间执行通信操作（自动路由，

__包括通过可用的NVLink）。默认情况下尚未启用此行为：新的代码途径已通过标准GROMACS回归  
测试进行验证，但（在发布时）仍然缺乏大量的“真实世界”测试。可以通过在shell中将以下环境  
变量设置为任何非空值来启用它们：GMX\_GPU\_DD\_COMMS（用于PP进程之间的环交换通信）；  
GMX\_GPU\_PME\_PP\_COMMS（用于PME和PP进程之间的通信）；还可以设置GMX\_FORCE\_\-  
UPDATE\_DEFAULT\_GPU以便与新的GPU更新功能（上文）相结合。这些组合（对于许多常见模  
拟）会在大多数时间步内将数据保留在GPU上，从而避免昂贵的数据传输。注意，这些功能当前需要  
使用内部线程MPI库而不是外部MPI库来构建GROMACS，并且仅限于单个计算节点。我们强调，用  
户应根据默认代码途径仔细验证结果，我们感激收到的任何问题报告，以帮助我们完善软件。__

##### GPU 上的成键内核已融合

##### 现在，不再为每种列出的相互作用类型启动一个GPU内核，而是使用一个GPU内核来处理所有列出

##### 的相互作用。在GPU上运行成键计算时这样做可以提高性能。

##### PP\-PME 调整中添加了提速延迟

##### 现代CPU和GPU可能需要几秒钟的时间才能提高时钟速度。因此，PP\-PME负载均衡现在会在 5 秒

##### 后启动，而不是在几个MD步骤后就启动。这可以避免次优的性能设置。

##### GROMACS 工具的改进

__修复 __: gmx order \-calcdist__ 中的错误__

##### 距离计算的参考位置计算错误。

__拒绝更多无效的 __\.mdp__ 行以提高 __grompp__ 可用性__

##### 像这样的行

__ref\-t 298 = 0\.1 =__

__现在都会被拒绝并给出说明信息，这可以防止构建\.mdp输入时出现某些类型的错误。注意，仍然接受缺  
少值的\.mdp参数名称，这种情况下该参数具有默认行为。__

__添加了 __convert\-trj____

__添加了新工具convert\-trj，用于转换轨迹格式，而无需使用旧版gmx trjconv。支持的操作包括生成精简  
的输出轨迹，以及使用结构文件中的数据替换各帧中的粒子信息。新工具支持命令行选区，这意味着不  
再需要编写index索引文件来选择某些原子。这是为了将trjconv工具拆分为更小的部分。__

__添加了 __extract\-cluster____

__添加了专用工具来提取从gmx cluster获得的不同簇所对应的轨迹帧。新的extract\-cluster工具可以生  
成新的轨迹，其中只包含与正确聚类相对应的帧。gmx trjconv中相应的选项 __\-sub__ 已移除。__

__改变了 __genion__ 的行为__

__改变genion的功能,以防止将与任何其他非溶剂原子的距离小于\-rmin的溶剂分子替换为离子。这一改  
进防止了离子可能被置于蛋白质中心的情况，这可能会导致折叠蛋白质不太稳定或可能需要很长的平衡  
时间。__

##### 错误修复

____gmx mdrun \-append__ 现在需要存在已有检查点__

__以前,当缺少检查点文件时，gmx mdrun \-append会从\.tpr构型启动\(因为不会追加\)\.__

____Verlet__ 缓冲现在可以正确处理微扰约束__

__对具有约束微扰的自由能计算，当微扰约束长度时，可能会低估Verlet缓冲区。由于通常只会微扰很少  
的约束，因此影响非常小，并且比由于近似而导致的缓冲区高估要小得多，因此大多数具有微扰约束的  
运行结果不会受到影响。__

__Issue 4395↪https://gitlab\.com/gromacs/gromacs/\-/issues/4395__

__GROMACS核心团队希望让用户和下游开发人员了解即将发生的变化，以便最大限度地减少干扰。如果  
你觉得计划有不当之处，请联系我们！__

__已废弃的功能通常会在GROMACS中保留一年或更长时间，但不应依赖这一点。__

##### GROMACS 2020 预期的功能变化

__gmx mdrun \-membed__

__会保留将蛋白质嵌入膜中的功能，但可能会采取不同的形式，例如gmx membed\.__

__gmx mdrun \-rerun__

__从轨迹计算势能量的功能会保留，但可能会采取不同的形式，例如 gmx rerun 和 gmx  
test\-particle\-insertion\.__

__积分器 __\.mdp__ 选项会只包含动力学积分器__

__将以不同的形式访问能量最小化，可能会使用gmx minimize,并解读一个\.mdp字段以确定要使用最小  
化方法。可以使用gmx normal\-modes之类来访问简正模式分析。这些工具的命令行帮助可以能够更好  
地记录何时支持哪些功能。__

__trjconv,editconf,eneconv 和 trjcat 中有很多功能__

##### 正在分离此类工具中的功能，以使其能用于可组合模块，我们计划将其作为更简单的工具，并最终通过

##### 正在开发的GROMACS API提供。

__gmx do\_dssp 会被替代__

__该工具已废弃，因为某些用户获取并安装单独的DSSP二进制文件时会出现问题，因此我们计划在某个  
时候用原生实现（可能基于xssp）替换该工具，并使用新的gmx工具名称。__

##### GROMACS 2020 中废弃的功能

##### 支持 32 位架构

##### 当前或计划中没有使用 32 位架构的大规模资源，我们无法正确测试和评估它们。

__Issue 3252↪https://gitlab\.com/gromacs/gromacs/\-/issues/3252__

##### 48 次幂的自由能软核函数

##### 48 次幂的自由能软核函数几乎从未使用过，因此废弃。

__Issue 3253↪https://gitlab\.com/gromacs/gromacs/\-/issues/3253__

__支持 __Armv7____

##### 对于该架构,当前代码存在多个问题，并且我们没有资源来支持和修复与其相关的问题。由于该架构对

##### HPC影响不大，因此废弃。

__Issue 2990↪https://gitlab\.com/gromacs/gromacs/\-/issues/2990__

##### GROMACS 2019 中废弃的功能

##### 生成虚拟位点以替代标准残基中的芳环

##### 这些功能被认为在某些情况下会产生假象（未发表的结果），并且从未经过充分测试，也未广泛使用，我

__们还需要简化pdb2gmx。__

__Issue 3254↪https://gitlab\.com/gromacs/gromacs/\-/issues/3254__

__基准测试选项仅适用于 __gmx benchmark____

__诸如\-confout,\-resethway,\-resetstep 之类的选项不适合普通mdrun用户使用，因此只能通过专  
用工具使用它们会更清楚。此外，这允许我们自定义默认值，例如以适合各自mdrun和基准用例的方式  
在模拟部分末尾写入文件，因此不再需要\-confout。__

__Issue 3255↪https://gitlab\.com/gromacs/gromacs/\-/issues/3255__

__gmx mdrun \-nsteps__

__\.tpr文件说明的模拟步数可以使用 gmx convert\-tpr 进行更改，或者在调用 gmx grompp 之前修  
改\.mdp文件中的值。这个mdrun选项虽有便利性,但其实现质量可疑、日志文件中没有明确记录并缺  
乏维护。__

__Issue 3256↪https://gitlab\.com/gromacs/gromacs/\-/issues/3256__

##### 移除的功能

##### 组截断方案

##### 已移除组截断方案\.几类依赖于它的模拟无法正常工作:

##### • 不支持真空条件下的模拟。

##### • 不支持用户提供短程非键相互作用的表格。

- __Switched short\-range nonbonded interactions with PME are not supported\.不支持PME与切换  
短程非键相互作用同用。__
- __停用膜嵌入。__
- __不支持QMMM\.  
Issue 1852↪https://gitlab\.com/gromacs/gromacs/\-/issues/1852__

##### 广义反应场

##### 这仅适用于组方案。注意，仍然可以使用标准反应场并手动计算介电常数来执行广义反应场模拟。

____gmx anadock____

__已移除gmx anadock工具，因为它不属于gromacs（它分析AutoDock的输出）。__

____gmx dyndom____

__已移除gmx dyndom工具,因为它不属于gromacs（它分析DynDom的输出）。__

____gmx morph____

__已移除gmx morph工具，因为它生成无物理意义的结构,且可以通过脚本轻松完成。__

____gmx mdrun \-gcom____

__此功能有时会以难以理解和报告的方式覆盖各种\.mdp设置的效果。用户如果想要较少地在PP进程之  
间进行通信,应该相应地选择nst\*mdp选项。__

##### 可移植性

__添加了对 __Hygon Dhyana CPU__ 架构的支持__

__对源自第一代AMD Zen的Hygon Dhyana,已支持硬件检测和相关启发，并与其共享大部分架构细节。__

__在 __NVIDIA__ 和 __Intel GPU__ 上使用 __OpenCL__ 支持 __PME__ 卸载__

__由于可移植性的改进，之前禁用的PME OpenCL卸载现在也可以在NVIDIA和Intel GPU上启用。__

##### 466 第 7 章 发布注记

__修复了使用 __GCC__ 在 __Solaris__ 上构建的问题__

__GROMACS现在可以使用GCC在Solaris上构建（在illumos发行版openindiana、“Hipster”滚动版  
本上进行了测试，使用GCC 5、 6 、 7 和 8 ）。__

##### 杂项

__如果 __mdp__ “ __define__ ”段中的宏未在拓扑中使用， __grompp__ 现在会发出警告__

__如果解析拓扑文件时未遇到mdp中定义的宏（例如\-DPOSRES），现在会引发grompp警告__

__Issue 1975↪https://gitlab\.com/gromacs/gromacs/\-/issues/1975__

__引入了 __CMake__ 变量 __GMX\_VERSION\_STRING\_OF\_FORK____

##### 为了帮助用户和开发人员理解正在使用哪个版本的GROMACS，任何提供GROMACS分叉版本的人都

__应在源代码中设置GMX\_VERSION\_STRING\_OF\_FORK（或者运行CMake时有必要的话）。它会  
出现在日志文件中，这样用户可以知道结果是哪个版本和分支的代码产生的。__

##### 提供校验码来验证发布的压缩包

##### GROMACS的发布版本现在会提供校验码,这是根据参与构建二进制文件的文件计算出的。从压缩包构

##### 建GROMACS时，会再次计算文件的校验码，并与发布构建期间生成的校验码进行比较。如果校验码

##### 不匹配，会修改版本字符串以指示源码树已被修改，并将该信息打印在用户的日志文件中。如果无法进

__行校验（由于安装过程中缺少Python，或者由于缺少原始校验码文件），则会通过不同的版本字符串来  
指示。__

__Issue 2128↪https://gitlab\.com/gromacs/gromacs/\-/issues/2128__

##### 物理常数更新到 CODATA 2018

##### 如果软件保持最新标准，会更容易实现计算结果的重复性。因此，标准单位的值已更新，以符合

__CODATA↪http://www\.codata\.org/committees\-and\-groups/fundamental\-physical\-constants提供的数据。__

__将 __grompp__ 关于无 __SD__ 进行去耦合的警告更改为注释__

__不使用SD积分器对分子进行去耦合时, grompp发出的警告已改为注释，因为存在使用正常MD,不在  
完全解耦状态下运行的实际用例\.__

__Issue 2767↪https://gitlab\.com/gromacs/gromacs/\-/issues/2767__

### 8\.2 简介

#### 8\.2\.1 计算化学与分子建模

##### GROMACS是一个用于执行分子动力学模拟和能量最小化的引擎。分子动力学模拟和能量最小化是计

##### 算化学和分子建模领域众多技术之中的两种。计算化学这个名称表明了它是计算技术在化学中的应用，

##### 涉及的范围从分子的量子力学到复杂大分子聚集体的动力学。分子建模是指用近真实的原子模型描述复

##### 杂化学系统的一般过程，其目的是根据原子尺度的详细知识来理解和预测物质的宏观性质。通常，分子

##### 建模用于设计新材料，为此就需要对实际系统的物理性质进行准确的预测。

##### 宏观物理特性可以分为

##### 1\.静态平衡性质，如抑制剂与酶的结合常数，系统的平均势能，或液体的径向分布函数，以及

##### 2\.动态或非平衡性质，如液体的粘度，膜中的扩散过程，相变的动力学，反应动力学或晶体缺陷的动

##### 力学。

##### 计算方法的选择取决于要回答的问题以及该方法在当前技术水平下得到可靠结果的可行性。理想情况

##### 下，（相对论性）含时薛定谔方程能以很高的精度描述分子系统的性质，但是这种从头算水平的方法只

##### 能处理几个原子的平衡态。因此，采用近似是必要的；系统的复杂度越高，待研究过程的时间跨度越

##### 长，计算所需的近似度就越高。到了某个阶段（远早于人们所期望的），从头算方法必须借助于所用模

##### 型的经验参数，或被其取代。当系统的复杂度过高，基于原子间相互作用的物理原理进行模拟仍会失败

##### 时，分子模拟却完全建立在对已知结构和化学数据进行相似性分析的基础之上。定量构效关系（QSAR，

__Quantitative Structure\-Activity Relations）方法和许多基于同源蛋白的蛋白质结构预测都属于这类方  
法。__

__宏观性质始终是分子系统某种代表性统计系综（平衡或非平衡）的系综平均值。对分子建模而言，这预  
示着两个重要推论：__

- __仅了解单一结构，即便它对应于全局能量最小点，也是不够的。为计算宏观性质，必须在给定温度  
下产生有代表性的系综。但对于计算那些与自由能相关的热力学平衡性质，如相平衡，结合常数，  
溶解度，分子构象的相对稳定性等，这仍然不够。计算自由能和热力学势需要对分子模拟技术进行  
特殊的扩展。__
- __原则上，分子模拟提供了体系结构和运动的原子尺度的细节，然而，这些细节却往往与感兴趣的宏  
观性质无关。这为简化相互作用的描述并对无关细节进行平均提供了途径。统计力学为这些简化提  
供了理论框架。这些方法存在一种层次等级结构，从将一组原子视为一个单元，以较少的集约坐标__

__描述运动，对溶剂分子利用平均力势结合随机动力学进行统计平均 \(^9\) ↪ 704 ，一直到介观动力学。介  
观动力学直接描述密度而不是原子，直接描述通量（作为对热力学梯度的响应）而不是速度或加速  
度（作为对力的响应） \(^10\) ↪ 704 。  
有两种方法可用于生成一个具有代表性平衡系综：  
1\.蒙特卡洛模拟  
2\.分子动力学模拟。  
对于非平衡系综的生成以及动态事件的分析，只有第二种方法是适用的。虽然与MD相比，蒙特卡洛模  
拟更简单（不需要计算力），但在给定的计算时间内，MC并不能得到明显好于MD的统计结果。因此，  
MD是一种更通用的方法。如果初始构型离平衡态很远，体系受力可能过大，MD模拟可能失败。在这  
种情况下，需要先对体系进行稳健的能量最小化。另一个进行能量最小化的原因是移除体系的所有动  
能：如果必须对动态模拟中的几个“快照”进行比较，能量最小化能够降低结构和势能中的热噪声，因  
此比较结果会更好。__

__我们可以将键（和键角）视为运动方程中的约束。其理由是，处于基态的量子谐振子更接近受约__

__束的键，而不是经典的谐振子。这样做有一个很好的实际理由，当移除最高频率后，算法可以使用__

__更大的时间步长。在实践中，相比将键视为谐振子，将其视为约束时时间步长可以取为原来的四__

__倍 \(^12\) ↪ 704 。GROMACS对键和键角提供了约束选项。灵活的键角约束相当重要，它使得构形空间的  
运动以及覆盖更加真实 \(^13\) ↪ 704 。  
电子处于基态  
在MD中，我们使用保守力场，它只是原子位置的函数。这意味着没有考虑电子的运动：当原子位置发  
生变化时，电子能够瞬间调整自己的运动状态（ Born\-Oppenheimer 近似），并仍然处于其基态。这个假  
定真的很好，几乎总是成立。但显然不能用于处理电子转移过程和电子激发态，也不能正确地处理化学  
反应。但我们暂时回避反应还有其他的原因。  
力场是近似的  
力场提供了力。实际上它们并不是模拟方法的一部分。当需要或对体系有了更多了解后，用户可以修改  
力场中的参数。但是，在特定程序中所能使用的力的函数形式是有限制的。GROMACS中的力场将在第  
4 章进行说明。在目前的版本中，力场是成对累加的（长程库仑力除外），不能包含极化，也不包含可以  
微调的成键相互作用。由此还导致了下面列出的一些限制。除此之外，力场对水溶液中的生物大分子非  
常有用，而且相当可靠\!  
力场是成对累加的  
这意味着，所有的非键力都来自于非键对势相互作用的加和。非对势累加的相互作用中最重要的例子是  
通过原子极化产生的相互作用，它可以由有效对势进行描述，但仅包含了非对势累加的平均贡献。这也  
意味着，成对相互作用并不纯，即，它们不适用于孤立的原子对，对那些与参数化时所基于的模型有明  
显差异的体系也是无效的。实际上，有效对势在实际应用中并没有那么差。但忽略极化也就意味着原子  
中的电子无法正确地体现介电常数。举例来说，实际液态烷烃的介电常数略大于 2 ，这会减小（分数）  
电荷之间的长程静电相互作用。因此，模拟将高估长程库仑相互作用。幸运的是，下一近似稍稍弥补了  
这种影响。  
长程相互作用被截断  
本版本的GROMACS对Lennard\-Jones相互作用始终使用截断半径，对库仑相互作用有时也会使用截  
断半径。GROMACS使用的“最小映像约定”要求，对每项成对相互作用中的每个粒子，只考虑其在周  
期性边界条件下的一个映像，因此截断半径不能超过盒子大小的一半。对于大型系统来说，可使用的截  
断半径仍然相当大，麻烦在于含有带电粒子的系统。这种情况下，可能会发生非常糟糕的事情，比如电  
荷会在截断边界出累积，或计算的能量完全错误\!对于这样的系统，应该考虑使用长程静电相互作用算  
法，如粒子网格Ewald \(^14\) ↪ 704 ， \(^15\) ↪ 704 。  
边界条件不自然  
由于系统尺寸较小（即使含 10000 个粒子的体系也仍然很小），粒子簇与其环境（真空）之间会产生许  
多不需要的边界。如果要模拟体相系统，我们必须避免这种情况。因此，我们使用周期性边界条件来避  
免真实的相边界。但由于液体不是晶体，因此仍然存在一些不自然的情况。我们最后提及这一方面是因  
为它的影响最小。对大系统，其误差很小，但对于具有大量内部空间相关性的小系统，周期边界可能会  
增强其内部相关性。在这种情况下，要多加小心并注意测试系统尺寸的影响。当使用晶格加和方法计算  
长程静电相互作用时，这一点尤其重要，因为我们已经知道这样做有时会导致系统产生额外的有序性。__

#### 8\.2\.3 能量最小化与搜索方法

##### 正如在计算化学与分子建模↪ 471 一节中提到的，许多情况下需要进行能量最小化。GROMACS提供了许

##### 多进行局部能量最小化的方法，详见能量最小化↪ 512 一节。

##### （大）分子系统的势能函数是多维空间中的一个超曲面，具有非常复杂的形貌。它有一个最低点，即全

##### 局极小值和大量的局部极小值。在这些点上，势能函数对所有坐标的导数都为零，并且所有的二阶导数

__都是非负的。二阶导数组成的矩阵称为 Hessian 矩阵，它具有非负特征值；只有对应于（孤立分子）平__

__动和转动的集约坐标具有零特征值。局部极小点之间存在鞍点，其Hessian矩阵仅有一个负的特征值。__

__通过这些点系统可以从一个局部极小点转移到另一个局部极小点。__

__拥有所有局部极小点，包括全局极小点，和所有鞍点的信息，我们就可以描述相关的结构和构象，它们__

__的自由能，以及结构转变的动力学。遗憾的是，构型空间的维数太高，局部极小点的数目太多，以至于__

__我们不可能对构型空间进行足够的采样，从而获得完整的信息。特别是，没有一种最小化方法能保证在__

__实际可以承受的时间范围内确定全局最小点。也存在一些不很实用的方法，速度有快有慢 \(^16\) ↪ 704 。然而，  
给定一个初始构型，可以找到它的最近局部极小点。这里的“最近”并不总是意味着结构意义上的“最  
近”（即坐标差的平方和最小），而是指通过系统地沿局部梯度最陡方向往下移动所能达到的极小点。很  
抱歉，GROMACS能为你做的只是找到这种最近局部极小点\!如果你想找到其他极小点，并希望在此过  
程中发现全局极小点，最好尝试下温度耦合MD:先将体系在高温下模拟一段时间，然后将其慢慢冷却  
至所需的温度；并不断重复这一过程\!如果存在熔点或玻璃化转变温度，更明智的做法是，先在略低于  
该温度的条件下模拟一段时间，再根据某些聪明的方案慢慢降温，这一过程被称为模拟退火。由于这一  
过程不需要与真实的物理过程相对应，你可以尽量发挥自己的想象力来加速这一过程。一个经常使用的  
技巧是增加氢原子的质量（可增加到 10 左右）:虽然这会减慢氢原子其他方面的快速运动，却几乎不会  
影响系统中更慢的运动，同时能够将时间步长增大为原来的 3 或 4 倍。在搜索过程中你也可以修改势能  
函数，例如通过移除势垒（去除二面角函数或用软核势取代排斥势 \(^17\) ↪ 704 ），但要注意慢慢恢复为正确的  
势能函数。允许结构剧烈变化的最佳搜索方法是在四维空间中进行漫游 \(^18\) ↪ 705 ，但这超出了GROMACS  
的标准功能，需要一些额外的编程工作。  
有三类可行的能量最小化方法：__

- __只需要计算函数值的方法，如单纯形法及其变体。每一步前进都是在以前计算结果的基础上做出  
的。如果有导数信息可以利用，这类方法要比那些使用导数信息的方法差。__
- __使用导数信息的方法。由于在MD程序中，势能相对于所有坐标的偏导数（等于力的负值）都是  
已知的，因此由MD程序稍加修改而得到的这类方法非常合适。__
- __还使用二阶导数信息的方法。这些方法在极小点附近的收敛性非常好：二次势函数的极小化只需  
要一步\!问题在于，对于含𝑁个粒子的体系，必须对3𝑁 × 3𝑁的矩阵进行计算，存储，求逆。除  
非利用额外的编码获得二阶导数，否则的话，对大多数感兴趣的系统，这类方法都不可行。还有一  
些动态构建Hessian矩阵的中间方法，但它们也有存储需求过大的问题。因此GROMACS没有使  
用这类方法。  
GROMACS提供的最陡下降方法属于第二类方法。它只是简单地沿负梯度方向（也就是力的方向）前  
进，而不考虑先前已有的任何步骤。搜索过程中可以调整步长以便加快搜索速度，但搜索永远沿着能量  
降低的方向。这是一种简单稳健但有些蠢的方法：它的收敛速度可能相当慢，特别是处于局部极小点附__

__近时\!收敛更快的共轭梯度法（参见例如 \(^19\) ↪ 705 ）使用了前面步骤的梯度信息。一般来说，最陡下降法  
能够非常快地接近最近局部极小点，而共轭梯度法会能够找到非常接近局部极小点的点，但在远离极小  
点时表现较差。GROMACS也支持L\-BFGS最小化方法，这是几乎与共轭梯度法相当的方法，但在某  
些情况下其收敛速度更快。__

##### 每个元胞（立方体，长方体或三斜）都被 26 个平移的映像所包围。因此一个特定的映像始终可以用指

##### 向 27 个平移向量之一的索引来标识，并通过施加索引向量对应的平移来构建（参见计算力↪ 491 ）。限制

##### \(8\.14\)确保了只需要考虑 26 个映像。

#### 8\.4\.2 组的概念

##### GROMACS的MD和分析程序可对用户定义的原子组进行一些操作。组的最大数目为 256 ，但每个原

##### 子最多只能属于六类不同的组。这六类组如下：

##### 温度耦合组

##### 对每个温度耦合组可以单独定义温度耦合参数（参考温度，时间常数，自由度数目，参见蛙

##### 跳式积分方法↪ 492 ）。例如，在大分子溶液中，相比大分子，溶剂分子（力和积分的误差使其

##### 倾向于产生更多的热效应）与热浴耦合时可以使用更短的时间常数。又如，可以维持表面的

##### 温度低于吸附分子的温度。可以定义许多不同的温度耦合组。另请参见下面的质心组。

##### 冻结组

##### 属于冻结组的原子在模拟过程中保持静止。在平衡系统的过程中这是很有用的，例如可避免

##### 放置不当的溶剂分子对蛋白质原子产生不合理的碰撞，尽管对必须要保护的原子施加约束势

##### 可以达到同样的效果。如果需要，冻结选项可仅仅用于原子的一个或两个坐标方向，从而可

##### 以将原子冻结在一个平面或一条直线上。当一个原子被部分冻结时，即使在冻结方向上，它

##### 所受的约束仍然可以使它移动。一个完全冻结的原子不能被它所受的约束所移动。可以定义

##### 多个冻结组。冻结坐标不受压力缩放的影响；在某些情况下，这可能会导致不需要的结果，

##### 特别是与约束同用时（在这种情况下，得到的压力会非常大）。因此，建议避免将冻结组与约

##### 束以及压力耦合联合使用。为了平衡系统，可以先使用冻结进行等体积模拟，然后再使用位

##### 置限制和恒压模拟。这样做可能就足够了。

##### 加速组

__加速组中的每个原子会施加一个加速度 a 𝑔。这相当于一个质量权重的外力。利用这一特性可__

__驱使系统进入非平衡状态，并计算某些性质,如输运性质。__

__能量监测组__

__在模拟过程中，会考虑所有能量监测组之间的交叉相互作用。而且会分开计算Lennard\-Jones__

__项和Coulomb项。原则上，最多可以定义 256 个组，但这将会计算 256 × 256 项相互作用\!__

__所以最好谨慎地使用这个组。__

__成对的能量监测组之间的所有非键相互作用都可以排除（详细信息见“用户指南”）。来自被__

__排除的成对能量监测组的粒子对不会放入配对列表中。当不需要计算系统内部或部分之间的__

__相互作用时，这样做可以显著提高模拟速度。__

__质心组__

__GROMACS可以移除整个系统或原子组的质心（COM）运动。移除原子组的质心运行是有__

__用的，例如对摩擦力有限的系统（如气体系统），可以防止质心运动的发生。对温度耦合与质__

__心运动移除使用相同的组是合理的。__

__压缩位置输出组__

__为了进一步减小压缩轨迹文件（ xtc ↪ 621 或 tng ↪ 617 ），可以只存储一部分粒子的轨迹。所有指__

__定为压缩组的粒子会保存其轨迹，而其余粒子的轨迹不保存。如果未指定这样的输出组，所__

__有原子的坐标都将保存到压缩轨迹文件中。__

#### 8\.6\.2 参数文件

##### 原子

__原子类型的静态性质（参见表8\.11）是根据多个位置的数据指定的。质量来源于atomtypes\.atp文件  
（参见原子类型↪ 574 一节），电荷来源 rtp ↪ 615 （ rtp ↪ 615 = __r__ esidue __t__ opology __p__ arameter，残基拓扑参数，参  
见 rtp ↪ 615 一节）文件。这意味着只对构建氨基酸，核酸的基本单元定义的电荷，对其他的构建单元，用  
户需要自己定义电荷。当使用 pdb2gmx ↪ 297 程序生成拓扑↪ 617 文件时，来自这些文件的信息会整合到一  
起。  
__

##### 非键参数

__非键参数包括范德华参数V（c6或𝜎，取决于组合规则）和W（c12或𝜖），它们列在ffnonbonded\.itp__

__文件中，其中ptype 为粒子类型（参见表8\.10）。与成键参数一样，\[ \*type \]指令中的条目会应用__

__到它们在拓扑文件中的对应部分。除了后面分子内的对相互作用↪ 580 一节中提到的那些参数，缺少参数__

__会导致警告。__

__\[ atomtypes \]__

__;name at\.num mass charge ptype V\(c6\) W\(c12\)__

__O 8 15\.99940 0\.000 A 0\.22617E\-02 0\.74158E\-06__

__OM 8 15\.99940 0\.000 A 0\.22617E\-02 0\.74158E\-06__

__\.\.\.\.\.__

__\[ nonbond\_params \]__

__; i j func V\(c6\) W\(c12\)__

__O O 1 0\.22617E\-02 0\.74158E\-06__

__O OA 1 0\.22617E\-02 0\.13807E\-05__

__\.\.\.\.\.__

__注意，GROMACS自带的大多数力场都包含at\.num\.列，但相同的信息在OPLS\-AA力场中隐含在__

__bond\_type列。参数V和W的含义取决于拓扑文件\[ defaults \]节段中选择的组合规则（参见拓扑__

__文件↪ 589 一节）:__

##### 成键参数

__成键参数（即键长，键角，反常和正常二面角）列在ffbonded\.itp文件中。这个数据库中的条目分  
别给出了参与相互作用的原子类型，相互作用的类型以及与该相互作用有关的参数。当处理拓扑时，  
grompp ↪ 252 程序会读取这些参数，并将其应用到相关的成键参数中，例如bondtypes会应用到\[ bonds  
\]节段中的条目，其他的类似。相关的：\[ \*type \]节段缺失任何成键参数都会导致致命错误。相互作  
用的类型列于表8\.14。下面是从这些文件中摘录的示例：__

__\[ bondtypes \]  
; i j func b0 kb  
C O 1 0\.12300 502080\.  
C OM 1 0\.12500 418400\.  
\.\.\.\.\.\.__

__\[ angletypes \]  
; i j k func th0 cth  
HO OA C 1 109\.500 397\.480  
HO OA CH1 1 109\.500 397\.480  
\.\.\.\.\.\.__

__\[ dihedraltypes \]  
; i l func q0 cq  
NR5\* NR5 2 0\.000 167\.360  
NR5NR5 2 0\.000 167\.360  
\.\.\.\.\.\.__

__\[ dihedraltypes \]  
; j k func phi0 cp mult  
C OA 1 180\.000 16\.736 2  
C N 1 180\.000 33\.472 2  
\.\.\.\.\.\.__

__\[ dihedraltypes \]  
;  
; Ryckaert\-Bellemans Dihedrals  
;  
; aj ak funct  
CP2 CP2 3 9\.2789 12\.156 \-13\.120\-3\.059726\.240 \-31\.495__

__在ffbonded\.itp文件中，你可以添加成键参数。如果你想为新的原子类型增加参数，请确保你已经在  
atomtypes\.atp中定义了它们。__

__对大多数相互作用类型，搜索和指定成键参数时，会对所有类型名称进行精确匹配，并且只允许一组参  
数。此规则的例外是二面角参数。对\[ dihedraltypes \]可以使用字母 X作为原子类型名称的通配  
符，它可以用于四个位置中的一个或多个。例如，可以根据中间两个原子的类型来指定正常二面角的参  
数。处理时会使用匹配最精确的条目的参数，即使用通配符匹配最少的条目。注意，GROMACS 5\.1\.3  
之前的版本使用首次匹配，这意味着，如果完全匹配项位于通配符匹配项的前面，那它将被忽略。因此，  
建议将通配符匹配条目放在最后，以防有人使用旧版本GROMACS的力场。此外，二面角类型 9 可以  
指定多个二面角势能，这适用于将具有不同多重度的多个项组合起来。不同的二面角势参数集应该位于  
\[ dihedraltypes \]节段中直接相邻的行。__

#### 8\.6\.3 分子定义

##### 分子类型条目

__通常对应于分子的一种组织结构是\[ moleculetype \]条目。这一条目有两个主要目的。一个是为拓扑  
文件提供结构，通常对应于实际分子。这使得拓扑更易读，并且编写起来也更简单省事。第二个目的是  
计算效率。计算机内存中存储的系统定义与moleculetype 定义的数目成正比。如果一个分子存在于  
100000 个副本中，节省的内存以 100000 计，这意味着系统通常可以放在缓存中，能极大地提高运行性  
能。对应于化学键的相互作用可能产生排除，只能在属于同一moleculetype内的原子之间进行定义。  
在一个moleculetype中允许存在多个分子，只要它们之间没有共价键连接。分子可以是无限长的，只  
要将其自身越过周期性边界相连接即可。当体系中存在这样的周期性分子时，需要在 mdp ↪ 612 文件中设  
置一个选项，告知GROMACS不要试图将跨越周期性边界的分子重新完整化。__

##### 分子间相互作用

##### 在某些情况下，人们希望不同分子中的原子之间也存在其他的相互作用，而不仅仅是通常的非键相互作

##### 用。在有关结合的研究中，这种情况很常见。当分子共价结合时，例如，配体与蛋白质共价结合时，它

__们实际上等同于一个分子，应该定义在同一个\[ moleculetype \]条目中。注意， pdb2gmx ↪ 297 有一个  
选项，可以将两个或多个分子置于同一\[ moleculetype \]条目中。当分子间不是共价结合时，使用单  
独的moleculetype定义，并在\[ intermolecular\_interactions \]部分指定分子间的相互作用更加  
方便。在位于拓扑文件（见表8\.13）末尾的这一部分中，可以使用全局原子索引来指定正常的成键相互  
作用。唯一的限制是不能使用可以生成排除的相互作用，也不能使用约束。__

##### 分子内的对相互作用

__一个分子中原子对之间额外的Lennard\-Jones和静电相互作用可以添加到分子定义的\[ pairs \]节段  
中。这些相互作用的参数可以独立地进行设置，与非键相互作用的参数可以不同。在GROMOS力场中，  
\[ pairs \]仅仅用于修改1\-4相互作用（相隔三条键的两个原子之间的相互作用）。在这些力场中，1\-4  
相互作用并未包含在非键相互作用中（参见排除↪ 580 一节）。__

__\[ pairtypes \]  
; i j func cs6 cs12 ; THESE ARE 1 \- 4 INTERACTIONS  
O O 1 0\.22617E\-02 0\.74158E\-06  
O OM 1 0\.22617E\-02 0\.74158E\-06  
\.\.\.\.\.__

__ffnonbonded\.itp文件中原子类型的配对相互作用参数位于\[ pairtypes \]节段。GROMOS力场明  
确地列出了所有这些相互作用的参数，但对于OPLS这样的力场这一节段可能是空的，因为这些力场通  
过统一地缩放参数来计算1\-4相互作用。对于那些不在\[ pairtypes \]节段出现的配对参数，只有当  
forcefield文件中\[ defaults \]指令的gen\-pairs设置为yes时才能生成（参见拓扑文件↪ 589 一  
节）。当gen\-pairs设置为no时， grompp ↪ 252 程序会对每个未设定参数的配对类型给出警告。__

__用于1\-4相互作用的正常配对相互作用的函数类型为 1 。函数类型 2 和\[ pairs\_nb \]用于自由能模  
拟。在计算水合自由能时，溶质需要从溶剂中解耦。这可以通过添加一个B状态拓扑（参见自由能计  
算↪ 514 一节）来完成，在这个状态下所有溶质的非键参数，即电荷和LJ参数，都设置为零。然而，A状  
态和B状态之间的自由能差并不是总的水合自由能。我们必须考虑到真空中溶质分子间的库仑和LJ相  
互作用，这些相互作用应当计入总的自由能。当溶质中的库仑和LJ相互作用不会改变时，第二步可以  
与第一步结合起来。为此，引入了配对函数类型 2 ，它与函数类型 1 完全相同，但B状态参数始终与  
A状态参数相同。当搜索\[ pairtypes \] 节段的参数时，函数类型 1 和 2 之间没有区别。配对相互  
作用节段\[ pairs\_nb \]用于取代非键相互作用。它使用未缩放的电荷和非键LJ参数；并只使用A状  
态的参数。注意，应该为\[ pairs\_nb \]节段中列出的所有原子对添加排除，否则这些原子对最终会出  
现在正常的邻区列表中。__

__或者，通过使用couple\-moltype，couple\-lambda0，couple\-lambda1和couple\-intramol关键字，  
可以不必修改拓扑而达到同样的目的。有关更多信息，请参见自由能计算↪ 514 一节和自由能计算的实  
现↪ 624 一节。__

__所有这三种配对类型全都使用普通的库仑相互作用，即便是使用反应场，PME，Ewald或移位库仑相互  
作用来计算非键相互作用时也是一样。类型 1 和类型 2 的能量会写入能量和日志文件，其中每对能量  
组都有单独的LJ\-14和Coulomb\-14项。\[ pair\_nb \]的能量会加到LJ\-\(SR\)和Coulomb\-\(SR\)项  
中。__

##### 排除

__grompp ↪ 252 会对彼此间相邻的键数不超过一定数目的原子生成非键相互作用的排除，并在拓扑文件的\[  
moleculetype \]节段中进行定义（参见拓扑文件↪ 589 一节）。当彼此之间通过“化学”键（\[ bonds \]  
类型至 5 ， 7 或 8 ）或约束（\[ constraints \] 类型 1 ）连接时，粒子被认为是键合在一起的。\[  
bonds \]类型 5 可用于在两个原子之间创建无相互作用的连接。有一种简谐相互作用（\[ bonds \]类  
型 6 ）可以不通过化学键将原子连接起来。还有一种第二约束类型（\[ constraints \]类型 2 ）可以  
维持固定的距离，但不通过化学键连接原子。所有这些相互作用的完整列表见表8\.14。__

__分子中额外的排除可以手动添加到\[ exclusions \] 节段中。每一行必须以一个原子索引号开始，后面  
跟着一个或多个原子索引号。第一个原子与其他原子之间的所有非键相互作用都会被排除。__

##### 当需要排除原子组内部或原子组之间的所有非键相互作用时，使用能量监测组进行排除更方便，也更有

##### 效（参见组的概念↪ 481 一节）。

#### 8\.6\.4 约束算法

__约束定义在\[ constraints \] 节段中。其格式为两个原子编号，后面跟着函数类型和约束距离。函数  
类型可以是 1 或 2 。它们之间的唯一区别在于，类型 1 可产生排除，而类型 2 不产生排除（参见排  
除↪ 580 一节）。距离是使用LINCS或SHAKE算法进行约束的，具体使用哪种算法可以在 mdp ↪ 612 文件  
中指定。在自由能计算中，通过增加第二个约束距离，这两种类型的约束都可以进行微扰（参见约束  
力↪ 602 一节）。 grompp ↪ 252 程序可以自动将一些类型的键和键角（参见表8\.14）转换为约束。 mdp ↪ 612 文  
件中有几个相关的选项。__

#### 8\.6\.5 pdb2gmx 输入文件

__GROMACS的 pdb2gmx ↪ 297 程序可以根据输入的坐标文件生成拓扑。它支持几种不同格式的坐标文件，  
但 pdb ↪ 614 是最常用的（因此程序命名为 pdb2gmx ↪ 297 ）。运行时， pdb2gmx ↪ 297 程序会在GROMACS的  
share/top目录以及工作目录的子目录中搜索力场，并根据扩展名为\.ff的目录中的forcefield\.itp  
文件识别力场。如果目录中存在forcefield\.doc文件， pdb2gmx ↪ 297 会将此文件的第一行作为力场的  
简短描述显示给用户，以方便用户选择力场。否则，用户可以使用 pdb2gmx ↪ 297 的命令行参数\-ff xxx  
来选择力场，表示要使用位于xxx\.ff 目录中的力场。搜索力场时， pdb2gmx ↪ 297 会首先搜索工作目录，  
然后再搜索GROMACS的share/top目录，并使用找到的第一个匹配 xxx\.ff的目录。__

__pdb2gmx ↪ 297 会读入两个通用文件：位于力场目录的原子类型文件（扩展名 atp ↪ 608 ，参见原子类型↪ 574 一__

__节），以及来自工作目录或GROMACSshare/top目录的residuetypes\.dat文件。residuetypes\.dat__

__文件决定了哪些残基名称被视为蛋白质，DNA，RNA，水和离子。__

__pdb2gmx ↪ 297 可以读入一个或多个数据库中不同类型分子的拓扑信息。属于同一个数据库的一组文件应__

__具有相同的基准名称，基准名称最好能够对分子类型（如aminoacids，rna，dna）有所说明。可能的__

__数据库文件如下：__

__\.rtp__

__\.r2b（可选）__

__\.arn（可选）__

__\.hdb（可选）__

__\.n\.tdb（可选）__

__\.c\.tdb（可选）  
只有包含了构建单元拓扑信息的 rtp ↪ 615 文件是必需的。其他文件中的信息只用于具有相同基准名称  
的 rtp ↪ 615 文件中的构建单元。通过在工作目录中放置具有相同基准名称的额外文件，用户也可以将新的  
构建单元添加到力场中。默认情况下只能定义额外的构建单元，但使用\-rtpo选项调用 pdb2gmx ↪ 297 时  
允许使用工作目录文件中的构建单元来代替力场中默认的构建单元。__

##### 残基数据库

__残基数据库文件的扩展名为 rtp ↪ 615 。最初，这个文件包含蛋白质的构建单元（氨基酸），是GROMACS  
对GROMOSrt37c4\.dat 文件的解释说明。因此，残基数据库文件包含常用构建单元的信息（键，电  
荷，电荷组和反常二面角）。最好不要修改这个文件，因为它是 pdb2gmx ↪ 297 的标准输入。但如果确实  
需要修改，请修改 top ↪ 617 文件（参见拓扑文件↪ 589 一节），或修改工作目录中的 rtp ↪ 615 文件，像前面的  
说明那样。直接编写包含拓扑文件 itp ↪ 611 来定义一个新的小分子的拓扑可能更容易一些。具体作法将  
在 Molecule\.itp 文件↪ 598 一节说明。当向数据库中添加新的蛋白质残基时，不要忘了将残基名称添加到  
residuetypes\.dat文件中，这样 grompp ↪ 252 ， make\_ndx ↪ 270 和分析程序才能将残基识别为蛋白质残基  
（参见默认组↪ 678 一节）。__

__rtp ↪ 615 文件只用于 pdb2gmx ↪ 297 程序。正如前面提到的，这个程序只需要从 rtp ↪ 615 数据库中读入键，原__

__子电荷，电荷组和反常二面角这些额外信息，因为其余信息是从坐标输入文件中读入的。一些蛋白质含__

__有非标准残基，而且坐标文件中列出了这些非标准残基。你必须为这个“奇怪的”残基创建一个构建单__

__元，否则你无法得到 top ↪ 617 文件。对坐标文件中的一些其他分子，如配体，多原子离子，结晶溶剂分子__

__等，也需要同样做。残基数据库的创建方式如下：__

__\[ bondedtypes \] ; mandatory__

__; bonds angles dihedrals impropers__

__1 1 1 2 ; mandatory__

__\[ GLY \] ; mandatory__

__\[ atoms \] ; mandatory__

__; name type charge chargegroup__

__N N \-0\.280 0__

__H H 0\.280 0__

__CA CH2 0\.000 1__

__C C 0\.380 2__

__O O \-0\.380 2__

__\[ bonds \] ; optional  
;atom1 atom2 b0 kb  
N H  
N CA  
CA C  
C O__

__C N__

__\[ exclusions \] ; optional  
;atom1 atom2__

__\[ angles \] ; optional  
;atom1 atom2 atom3 th0 cth__

__\[ dihedrals \] ; optional  
;atom1 atom2 atom3 atom4 phi0 cp mult__

__\[ impropers \] ; optional  
;atom1 atom2 atom3 atom4 q0 cq  
N \-C CA H__

__C \-CA N \-O__

__\[ ZN \]__

__\[ atoms \]__

__ZN ZN 2\.000 0__

__文件是自由格式；唯一的限制是每行最多只能有一个条目。文件中的第一个节段为 \[ bondedtypes \]  
节段，后面跟着四个数字，分别代表键，键角，二面角和反常二面角的相互作用类型。文件中的残基条目  
包含原子和（可选的）键，键角，二面角和反常二面角。电荷组代码代表电荷组的编号。同一电荷组中  
的原子应该始终按顺序连续排列。当 pdb2gmx ↪ 297 程序使用氢数据库添加缺失的氢原子时（参见 hdb ↪ 611 ），  
rtp ↪ 615 条目中定义的氢原子名称应该与氢数据库中使用的命名约定完全一致。成键相互作用中的原子名  
称前可以添加负号或正号，分别代表原子位于前一残基或后一残基。添加到键，键角，二面角和反常二  
面角的显式参数会覆盖 itp ↪ 611 文件中的标准参数。这种做法只应该用于特殊情况。也可以为每个成键相  
互作用添加字符串，而不是参数。GROMOS\-96的 rtp ↪ 615 文件就是这样。这些字符串会复制到拓扑文件  
中，通过使用 grompp ↪ 252 C预处理器的\#define语句，就可以用力场参数替换这些字符串。__

__pdb2gmx ↪ 297 程序会自动生成所有的键角。这意味着对大多数力场，\[ angles \]节段仅用于覆盖 itp ↪ 611  
参数。对GROMOS\-96力场必须指定所有键角的相互作用编号。__

__pdb2gmx ↪ 297 程序会自动为每个可旋转的键生成一个正常二面角，并倾向位于重原子上。当使用 \[  
dihedrals \]节段时，不会为与指定二面角对应的键生成其他二面角。可以为一条可旋转的键指定一个  
以上的二面角函数。对CHARMM27力场，使用 pdb2gmx ↪ 297 程序默认的\-cmap选项可以为二面角添  
加校正映射。更多信息，请参考 CHARMM ↪ 573 。__

__pdb2gmx ↪ 297 会将排除数设置为 3 ，这意味着最多 3 条键连接的原子之间的相互作用会被排除。程序会__

__为相隔 3 条键的所有原子对生成配对相互作用（氢原子对除外）。当需要排除更多的相互作用，或不需__

__要生成某些配对相互作用时，可以添加\[ exclusions \] 节段，后面跟着位于不同行上的原子名称对。__

__这些原子之间的所有非键和配对相互作用都将被排除。__

##### 残基 \- 构建单元转换数据库

##### 每个力场都有自己的残基命名约定。大多数残基的命名是一致的，但有些残基，特别是那些具有不同质

__子化状态的残基，可能具有许多不同的名称。 r2b ↪ 616 文件可用于将标准残基名称转换为力场构建单元的  
名称。如果力场目录中不存在 r2b ↪ 616 文件，或有残基未列出，会假定构建单元的名称与残基名称完全相  
同。 r2b ↪ 616 文件可包含 2 或 5 列。 2 列格式为：第一列为残基名称，第二列为构建单元名称。 5 列格式  
有 3 个附加列，分别为出现在N端，C端，同时出现在两个末端的残基（单个残基分子）对应的构建单  
元的名称。这适用于一些力场，如AMBER力场。如果不存在一个或多个末端状态，应在相应列中输入  
短划线。  
GROMACS对残基有自己的命名约定，这个约定只通过 r2b ↪ 616 文件和specbond\.dat 文件表现出来  
（ pdb2gmx ↪ 297 代码除外）。只有当将残基类型添加到 rtp ↪ 615 文件时，这个约定才变得非常重要。此约定  
列在表8\.12中。对于特殊的键，如与血红素相关的键，GROMACS命名约定通过specbond\.dat引入  
（参见特殊键↪ 588 一节），如果需要，此约定随后可以利用 r2b ↪ 616 文件进行转换。__

__表8\.12: GROMACS内部的残基命名约定。__

__GROMACS名称 残基__

__ARG 质子化精氨酸__

__ARGN 中性精氨酸__

__ASP 带负电荷的天冬氨酸__

__ASPH 中性天冬氨酸__

__CYS 中性半胱氨酸__

__CYS2 通过硫结合到另一个半胱氨酸或血红素的半胱氨酸__

__GLU 带负电荷的谷氨酸__

__GLUH 中性谷氨酸__

__HISD N𝛿质子化的中性组氨酸__

__HISE N𝜖质子化的中性组氨酸__

__HISH N𝛿和N𝜖质子化的带正电荷的组氨酸__

__HIS1 与血红素结合的组氨酸__

__LYSN 中性赖氨酸__

__LYS 质子化赖氨酸__

__HEME 血红素__

原子重命名数据库

__力场中使用的原子名称通常不遵循IUPAC或PDB约定。 arn ↪ 608 数据库用于将坐标文件中的原子名称__

__转换为力场中的原子名称。数据库中未列出的原子会保留其原有名称。该数据库文件有三列：构建单元__

__名称，旧的原子名称，新的原子名称。残基名称支持问号通配符，用以匹配单个字符。__

__share/top目录下还存在一个通用的原子重命名文件xlateat\.dat，它可以将坐标文件中常见的非标__

__准原子名称转换为IUPAC/PDB约定名称。因此，在编写力场文件时，可以假定原子具有标准原子名__

__称，除了将标准名称转换为力场名称外，不需要进一步的转换。__

##### 氢原子数据库

__氢原子数据库存储在 hdb ↪ 611 文件中。它包含了 pdb2gmx ↪ 297 程序如何将氢原子连接到已有原子的相关信  
息。在GROMACS 3\.3版本之前的数据库中，氢原子是根据它们所连接的原子进行命名的：将连接原子  
名称的首字母替换为H。从3\.3版本开始，必须明确列出氢原子，因为以前的作法仅适用于蛋白质，因  
而不能推广用于其他分子。如果一个以上的氢原子连接到同一个原子，氢原子名称的末尾会添加一个数  
字。例如，添加两个氢原子到（天冬酰胺中的）ND2，它们将被命名为HD21和HD22。这很重要，因  
为 rtp ↪ 615 文件（参见 rtp ↪ 615 一节）中的原子命名必须相同。氢原子数据库的格式如下：__

__; res \_\# additions__

__H add type H i j k\___

__ALA 1  
1 1 H N \-C CA  
ARG 4  
1 2 H N CA C  
1 1 HE NE CD CZ  
2 3 HH1 NH1 CZ NE  
2 3 HH2 NH2 CZ NE__

__第一行为残基名称（ALA或ARG）以及氢原子的类型数，这些氢原子可以根据氢原子数据库添加到残基  
中。后面的每行对应于一次氢原子的添加：__

__添加的氢原子数__

__添加氢原子的方法，可能的方法如下：  
1\.单个平面氢原子，如环或肽键  
添加一个氢原子（n），置于原子\(i, j, k\)形成的平面内，位于角\(j\-i\-k\)的平分线上，距原子i  
0\.1 nm，并使得角\(n\-i\-j\)和\(n\-i\-k\)> 90 o。  
2\.单个氢原子，如羟基  
添加一个氢原子（n），距原子i 0\.1 nm，并使得角\(n\-i\-j\)为109\.5o，二面角\(n\-i\-j\-k\)为反式。  
3\.两个平面氢原子，如乙烯 \-C=CH 2 ,或酰胺 \-C\(=O\)NH 2  
添加两个氢原子\(n1, n2\)，距原子i 0\.1 nm，并使得角\(n1\-i\-j\)和\(n2\-i\-j\)都为 120 o，二面角__

__\(n1\-i\-j\-k\)为顺式，\(n2\-i\-j\-k\)为反式，这样命名符合IUPAC标准 \(^129\) ↪ 711 。  
4\.两个或三个四面体氢原子，如 \-CH 3  
添加三个\(n1, n2, n3\)或两个\(n1, n2\)氢原子，距原子i 0\.1 nm，并使得角\(n1\-i\-j\), \(n2\-i\-j\)  
和\(n3\-i\-j\)都为109\.47o，二面角\(n1\-i\-j\-k\)为反式，\(n2\-i\-j\-k\)为反式\+120o, \(n3\-i\-j\-k\)为反  
式\+240o。  
5\.单个四面体氢原子，如 C 3 \-CH  
添加一个氢原子\(𝑛′\)，距原子i 0\.1 nm，处于四面体构型中，角\(𝑛′\-i\-j\), \(𝑛′\-i\-k\), \(𝑛′\-i\-l\)都是  
109\.47o。  
6\.两个四面体氢原子，如 C\-CH 2 \-C  
添加两个氢原子\(n1, n2\)，距原子i 0\.1 nm，处于四面体构型中，位于平分角j\-i\-k的平面上，  
并且角为\(n1\-i\-n2\), \(n1\-i\-j\), \(n1\-i\-k\)都为109\.47o。  
7\.两个水中的氢原子  
根据SPC水模型 \(^80\) ↪ 708 的几何构型，在原子i周围添加两个氢原子。对称轴的两个方向交替__

##### 地位于三个坐标轴之间。

##### 8\.三个水中的“氢”原子

__根据SPC水模型 \(^80\) ↪ 708 的几何构型，在原子i周围添加两个氢原子。对称轴的两个方向交替  
地位于三个坐标轴之间。此外，在氧原子位置上添加一个额外的粒子，并将其名称的第一个  
字母以M代替。此方法适用于四位点的水模型，如TIP4P \(^128\) ↪ 711 。  
9\.四个水中的“氢”原子  
同上，但会在氧原子位置上添加两个额外的粒子，名称分别为LP1和LP2。此方法适用于五  
位点水模型，如TIP5P \(^130\) ↪ 711 。__

- __新的氢原子的名称（或其前缀，如前文天冬酰胺示例中的HD2）。__
- __三或四个控制原子\(i, j, k, l\)，其中第一个始终为与氢原子连接的原子。另外两个或三个取决于所  
选添加方法。对于水，只有一个控制原子。__

__对一些非常特殊的情况，可以利用上面的方法近似地构建，并进行适当的能量最小化，这样得到的构型  
作为MD模拟的初始构型足够好。例如对仲胺氢，亚硝酰基氢（C=NH），甚至乙炔氢，都可以利用上  
面添加羟基氢的方法 2 近似地构建。__

##### 末端数据库

__末端数据库存储在aminoacids\.n\.tdb和aminoacids\.c\.tdb文件中，分别对应于N端和C端。它们  
包含了 pdb2gmx ↪ 297 程序需要的一些信息：如何将新原子连接到已有原子，应删除或更改哪些原子，应  
添加哪些成键相互作用。文件的格式如下（来自gromos43a1\.ff/aminoacids\.c\.tdb）:__

__\[ None \]__

__\[ COO\-\]  
\[ replace \]  
C C C 12\.011 0\.27  
O O1 OM 15\.9994\-0\.635  
OXT O2 OM 15\.9994\-0\.635  
\[ add \]  
2 8 O C CA N  
OM 15\.9994\-0\.635  
\[ bonds \]  
C O1 gb\_5  
C O2 gb\_5  
\[ angles \]  
O1 C O2 ga\_37  
CA C O1 ga\_21  
CA C O2 ga\_21  
\[ dihedrals \]  
N CA C O2 gd\_20  
\[ impropers \]  
C CA O2 O1 gi\_1__

__文件以块的形式组织起来，每块的标题指定了块的名称。这些块对应于可以添加到分子中的不同末端的  
类型。在上面的例子中，\[ COO\- \]为第一块，对应于将末端碳原子更改为去质子化的羧基。\[ None \]  
为第二末端类型，对应于保持分子原状的末端。块名称不能取以下的任何一种：replace，add，delete，__

__bonds，angles，dihedrals，impropers。否则会干扰块的参数，并且可能也会让读者感到非常困惑。__

__每个块可使用以下选项：__

- __\[ replace \]  
将一个已有原子替换为具有不同原子类型，原子名称，电荷和/或质量的原子。此条目可用于替换  
同时存在于输入坐标和 rtp ↪ 615 数据库中的原子，也可用于只对输入坐标中的原子进行重命名，以  
使其与力场中的名称相匹配。对后一种情况，还应该提供相应的\[ add \]节段，用于指示如何添  
加相同的原子，这样才能知道序列中的位置和成键。这种原子可以存在于输入坐标中并保持不变，  
或不存在于输入坐标中而是通过 pdb2gmx ↪ 297 程序构建。对于每个要进行在线替换的原子，应算输  
入以下字段：  
__\-__ 要替换原子的名称  
__\-__ 新的原子名称（可选）  
__\-__ 新的原子类型  
__\-__ 新的质量  
__\-__ 新的电荷__
- __\[ add \]  
添加新的原子。对每个（组）要添加的原子，需要两行输入。第一行包含与氢原子数据库中的条目  
相同的字段（新原子的名称，原子数目，添加类型，控制原子，参见 hdb ↪ 611 ），但增加了两个添加  
类型，只用于C端：  
1\.两个羧基氧原子， \-COO −  
根据规则 3 添加两个氧原子\(n1, n2\)，距原子i 0\.136 nm，角\(n1\-i\-j\)，\(n2\-i\-j\)都是 117 度  
2\.羧基氧原子和氢原子， \-COOH  
根据规则 3 添加两个氧原子\(n1, n2\)，分别距原子i 0\.123 nm和0\.125 nm，角\(n1\-i\-j\)为  
121 度，角\(n2\-i\-j\)为 115 度。根据规则 2 在n2周围添加一个氢原子\(𝑛′\)，其中n\-i\-j和  
n\-i\-j\-k分别对应于n′\-n2\-i和n′\-n2\-i\-j。  
此行之后，接下来的另一行指定了添加原子的细节，与替换原子的方式相同，即：  
__\-__ 原子类型  
__\-__ 质量  
__\-__ 电荷  
__\-__ 电荷组（可选）  
如氢原子数据库（参见 rtp ↪ 615 一节）一样，当一个以上的原子连接到一个已有原子时，原子名称  
的末尾会追加一个数字。注意，就像在氢原子数据库中一样，原子名称现在与控制原子位于同一行  
中，而在GROMACS 3\.3版本之前它位于第二行的开头。当忽略电荷组字段时，添加的原子会与  
此原子所连接的原子具有相同的电荷组编号。__
- __\[ delete \]  
删除已有原子。每行一个原子名称。__
- __\[ bonds \]，\[ angles \]，\[ dihedrals \]和\[ impropers \]  
添加额外的成键参数。格式与 rtp ↪ 615 文件中使用的完全相同，参见 rtp ↪ 615 一节。__

##### 虚拟位点数据库

##### 由于不能依赖输入文件中氢的位置，我们需要一个特殊的输入文件来决定要添加的虚拟氢位点的几何构

##### 型和参数。为构建更复杂的虚拟位点（例如当保持整个芳族侧链刚性时），我们还需要侧链中所有原子

__平衡键长和角度的信息。这些信息在每个力场的 vsd ↪ 620 文件中指定。与末端类似， rtp ↪ 615 文件中的每个  
残基类别都有一个这样的文件。__

__虚拟位点数据库并不是一个非常简单的信息列表。它的前几个节段指定了用于CH 3 ，NH 3 和NH 2 基团  
的质量中心\(通常称为MCH 3 /MNH 3 \)。根据氢原子和重原子之间的平衡键长和键角，我们需要在这些  
质心之间施加略有不同的约束距离。注意，我们不需要指定实际的参数（会自动生成），而只需要指定  
要使用的质量中心类型。为此，有三个节段名称\[ CH3 \]，\[ NH3 \]和\[ NH2 \]。对每个节段，我们  
需要三列。第一列为连接到2/3氢的原子类型，第二列为连接的下一个重原子的类型，第三列为使用的  
质心类型。作为特例，\[ NH2 \]节段的第二列也可以指定为planar，代表使用不同的构建方法，并且  
不使用质心。目前，对于NH 2 基团是否应为平面结构，一些力场的观点不一，但我们尽量保持力场默认  
的平衡参数不变。__

__虚拟位点数据库的第二部分包含芳香族侧链的原子对/三联对的明确的平衡键长和键角。目前，虚拟位  
点生成代码中的特定例程会读取这些条目，因此如果你要扩展它，如扩展到核酸，你还需要编写新的代  
码。这些节段根据氨基酸的短名称进行命名（\[ PHE \]，\[ TYR \]，\[ TRP \]，\[ HID \]，\[ HIE \]，\[  
HIP \]），只包含 2 或 3 列：原子名称，接着是指定键长（以nm为单位）或键角（以度为单位）的数  
字。注意，这些是对整个分子平衡几何构型的近似，如果分子未处于平衡状态，其单个键长/键角的值可  
能与的平衡值不同。__

##### 特殊键

__pdb2gmx ↪ 297 程序生成残基间的化学键时使用的主要机制为，从头到尾连接不同残基中的骨架原子进而  
构成大分子。在某些情况下（如二硫键，血红素基团，支化聚合物），有必要创建残基间非骨架上的化学  
键。specbond\.dat文件用于实现这个功能。残基必须属于相同的 \[ moleculetype \]。当操控不同链  
之间特殊的残基间化学键时， pdb2gmx ↪ 297 程序的\-merge和\-chainsep选项非常有用。__

__specbond\.dat文件的第一行表示文件中的条目数。如果添加了新的条目，请确保增加此数字。文件中  
的其余行提供了创建键的说明。每行的格式如下：__

__resA atomA nbondsA resB atomB nbondsB length newresA newresB__

__每列分别表示：__

__resA:参与成键的残基A的名称。__

__atomA:残基A中成键原子的名称。__

__nbondsA:atomA可以成键的总数。__

__resB:参与成键的残基B的名称。__

__atomB:残基B中成键原子的名称。__

__nbondsB:atomB可以成键的总数。__

__length:键的参考长度。在提供给 pdb2gmx ↪ 297 程序的坐标文件中，若atomA和atomB之间的距  
离不在length±10%范围内，它们之间不会成键。__

__newresA:如果需要的话，残基A的新名称。有些力场使用诸如CYS2之类的名称来表示与二硫  
键或血红素相连的半胱氨酸。__

__newresB:残基B的新名称，同上。__

#### 8\.6\.6 文件格式

##### 拓扑文件

__拓扑文件是根据GROMACS分子拓扑的具体说明建立的。可利用 pdb2gmx ↪ 297 程序生成 top ↪ 617 文件。拓  
扑文件中所有可能的条目都列于表8\.13和8\.14。表中还列出了：所有参数的单位，哪些相互作用可用  
于自由能微扰计算， grompp ↪ 252 可使用哪些成键相互作用生成排除， grompp ↪ 252 可将哪些成键相互作用  
转换为约束。__

__参数__

__相互作用类型 指令 原子数（\#at\.） 函数类型（f\.tp） 参数__

__必需 defaults__

__非键函数类型；组合规则\(𝑐𝑟\);生成配对\(no/yes\); LJ校正因__

__子fudgeLJ\(\);库仑校正因子fudgeQQ\(\)__

__必需 atomtypes__

__原子类型；成键类型;原子序数;质量m\(u\);电荷q\(e\);粒子__

__类型；V\(𝑐𝑟\); W\(𝑐𝑟\)\(成键类型和原子序数为可选项\)__

__bondtypes （参见表8\.14bonds指令）__

__pairtypes （参见表8\.14pairs指令）__

__angletypes （参见表8\.14angles指令）__

__dihedraltypes\(∗\) （参见表8\.14dihedrals指令）__

__constrainttypes （参见表8\.14constraints指令）__

##### 系统

__必需 system 系统名称__

__必需 molecules 分子名称；分子数目__

### 8\.7 文件格式

#### 8\.7\.1 文件格式摘要

##### 参数文件

__mdp ↪ 612 运行参数， gmx grompp ↪ 252 和 gmx convert\-tpr ↪ 203 的输入文件__

__m2p ↪ 611 gmx xpm2ps ↪ 363 的输入文件__

##### 结构文件

__gro ↪ 610 GROMACS格式__

__g96 ↪ 609 GROMOS\-96格式__

__pdb ↪ 614 BrookHaven蛋白质数据库格式__

__结构 \+ 质量（ db ） : tpr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，或 pdb ↪ 614 ，用于分析工具的结构和质量输入。当使用  
gro或pdb时，将从质量数据库中读取近似质量。__

##### 拓扑文件

__top ↪ 617 系统拓扑（ascii文本）__

__itp ↪ 611 可引用拓扑（ascii文本）__

__rtp ↪ 615 残基拓扑（ascii文本）__

__ndx ↪ 613 索引文件（ascii文本）__

__n2t ↪ 614 原子命名定义（ascii文本）__

__atp ↪ 608 原子类型库（ascii文本）__

__r2b ↪ 616 残基到构建单元映射（ascii文本）__

__arn ↪ 608 原子重命名数据库（ascii文本）__

__hdb ↪ 611 氢原子数据库（ascii文本）__

__vsd ↪ 620 虚拟位点数据库（ascii文本）__

__tdb ↪ 616 末端数据库（ascii文本）__

__运行输入文件__

__tpr ↪ 619 系统拓扑，参数，坐标和速度（二进制，便携式）__

__轨迹文件__

__tng ↪ 617 任意类型的数据（压缩，便携，任意精度）__

__trr ↪ 619 x，v和f（二进制，全精度，便携式）__

__xtc ↪ 621 只含x（压缩，便携，任意精度）__

__gro ↪ 610 x和v（ascii文本，任意精度）__

__g96 ↪ 609 只含x（ascii文本，固定高精度）__

__pdb ↪ 614 只含x（ascii文本，降低精度）__

__全精度数据格式： tng ↪ 617 或 trr ↪ 619__

__通用轨迹格式： tng ↪ 617 ， xtc ↪ 621 ， trr ↪ 619 ， gro ↪ 610 ， g96 ↪ 609 ，或 pdb ↪ 614__

__能量文件__

__ene ↪ 609 能量，温度，压力，盒子大小，密度和维里（二进制）__

__edr ↪ 609 能量，温度，压力，盒子大小，密度和维里（二进制，便携式）__

__通用能量格式： edr ↪ 609 或 ene ↪ 609__

##### 其他文件

__dat ↪ 608 通用，更常用于输入__

__edi ↪ 609 用于 gmx mdrun ↪ 276 的本性动力学约束输入文件__

__eps ↪ 609 封装Postscript__

__log ↪ 611 日志文件__

__map ↪ 612 2019 版本中用于 gmx do\_dssp ↪ 225 的颜色映射输入文件__

__mtx ↪ 613 二进制矩阵数据__

__out ↪ 614 通用，更常用于输出__

__tex ↪ 616 LaTeX输入文件__

__xpm ↪ 620 ascii矩阵数据，可使用 gmx xpm2ps ↪ 363 转换为 eps ↪ 609__

__xvg ↪ 623 xvgr输入文件__

#### 8\.7\.2 文件格式详细信息

__atp__

__atp文件包含与原子类型有关的一般信息，如原子序数，原子质量（以原子质量单位为单位）。__

__arn__

__arn文件可以将原子的名称从力场名称重命名为IUPAC/PDB定义的名称，这样更容易进行可视化和识  
别。__

__cpt__

__cpt文件扩展名代表便携式检查点文件。模拟的完整状态存储在检查点文件中，包括扩展恒温器/恒压器  
变量，随机数状态以及NMR的时间平均数据。如果使用了区域分解，检查点文件中还会存储一些区域  
分解设置的信息。__

__另见 gmx mdrun ↪ 276 。__

__dat__

__具有dat扩展名的文件包含通用的输入或输出数据。由于无法对所有数据文件格式进行分类，GROMACS  
具有一种名为dat的通用文件格式，没有限定任何格式。__

__dlg: 2019 版本__

__dlg文件格式用作 gmx view ↪ 356 轨迹查看器的输入。这些文件不应由最终用户更改。__

__样本__

__grid 3918 \{__

__group"Bond Options" 11169 \{  
radiobuttons \{"Thin Bonds" "Fat Bonds""Very Fat Bonds""Spheres"\}  
"bonds""Ok""F""help bonds"  
\}__

__group"Other Options" 1812013 \{  
checkbox"Show Hydrogens" "" """FALSE""help opts"  
checkbox"Draw plus for atoms""" """TRUE" "help opts"  
checkbox"Show Box" "" """TRUE" "help opts"  
checkbox"Remove PBC" "" """FALSE""help opts"  
checkbox"Depth Cueing" "" """TRUE" "help opts"  
edittext"Skip frames: " "" """ 0 " "help opts"  
\}__

__simple 11537 2 \{  
defbutton"Ok""Ok""Ok""Ok""help bonds"  
\}__

__\}__

__edi__

__具有edi扩展名的文件包含的信息可用于 gmx mdrun ↪ 276 运行使用本性动力学约束的分子动力学。以前  
可以通过 WHAT IF↪https://swift\.cmbi\.umcn\.nl/whatif/ 程序提供的选项生成这种文件。__

__edr__

__edr文件扩展名代表便携式能量文件。文件使用xdr协议存储能量。__

__另见 gmx energy ↪ 237 。__

__ene__

__ene文件扩展名代表二进制能量文件。它保存了 gmx mdrun ↪ 276 运行期间生成能量。__

__这种文件可以转换为便携式能量文件（跨硬件平台的可移植性），只要使用 gmx eneconv ↪ 234 程序将其转  
换为 edr ↪ 609 文件即可。__

__另见 gmx energy ↪ 237 。__

__eps__

__eps文件格式不是特殊的GROMACS格式，只是标准PostScript\(tm\)的一种变体。由 gmx xpm2ps ↪ 363  
程序生成的示例eps文件如下。它显示了多肽的二级结构随时间的变化。__

__g96__

__具有g96扩展名的文件可以是GROMOS\-96格式的初始/最终构型文件，或坐标轨迹文件，或二者的组  
合。此文件是固定格式的，所有浮点数的输出格式都是15\.9（文件可能会变得非常大）。按给定的顺  
序，GROMACS支持以下数据块：__

__标题块：  
\- TITLE （必需）__

__帧块：  
\- TIMESTEP（可选）  
\- POSITION/POSITIONRED（必需）__

__– VELOCITY/VELOCITYRED（可选）__

__– BOX（可选）__

__有关块的完整说明，请参阅GROMOS\-96手册。__

__注意，所有GROMACS程序都可以读取压缩或gzip压缩文件。__

__gro__

__具有gro扩展名的文件包含Gromos87格式的分子结构。只要简单地连接起来，就可以将gro文件作为  
轨迹。程序会尝试从每帧的标题字符串中读取时间值，时间值应位于t=之后，如下面的示例所示。__

__示例如下：__

__MD of 2 waters, t=0\.0  
6  
1 WATER OW1 1 0\.126 1\.624 1\.679 0\.1227\-0\.0580 0\.0434  
1 WATER HW2 2 0\.190 1\.661 1\.747 0\.8085 0\.3191\-0\.7791  
1 WATER HW3 3 0\.177 1\.568 1\.613\-0\.9045\-2\.6469 1\.3180  
2 WATER OW1 4 1\.275 0\.053 0\.622 0\.2519 0\.3140\-0\.1734  
2 WATER HW2 5 1\.337 0\.002 0\.680\-1\.0641\-1\.1349 0\.0257  
2 WATER HW3 6 1\.326 0\.120 0\.568 1\.9427\-0\.8216\-0\.0244  
1\.82060 1\.82060 1\.82060__

__文本行包含以下信息（从上到下）:__

__标题字符串（自由格式的字符串，t =后可以是以ps为单位的时间）__

__原子个数（自由格式的整数）__

__每个原子一行（固定格式，见下文）__

__盒向量（自由格式，空格分开的实数），值：v1\(x\) v2\(y\) v3\(z\) v1\(y\) v1\(z\) v2\(x\) v2\(z\) v3\(x\) v3\(y\)，  
最后 6 个值可以省略（会被设置为零）。GROMACS只支持v1\(y\)=v1\(z\)=v2\(z\)=0的盒子。__

__这种格式是固定的，即所有列都处于固定位置。作为可选（现在只适用于trjconv），gro文件中小数的  
位数可以是任意的，这种情况下会有n\+5位，带有n 位小数（速度有n\+1位小数），而默认的格式是  
8 位其中 3 位为小数（速度的小数位数为 4 ）。在读取时，会根据小数点之间的距离（n\+5）推断数据  
的精度。文本列包含以下信息（从左到右）:__

__残基编号（ 5 位，整数）__

__残基名称（ 5 个字符）__

__原子名称（ 5 个字符）__

__原子编号（ 5 位，整数）__

__位置（以nm为单位，x y z三列，默认每个 8 位，包含 3 位小数）__

__速度\(以nm/ps\(或km/s\)为单位，x y z三列，默认每个 8 位，包含 4 位小数\)__

__注意，单独的分子或离子（如水或Cl\-）被视为残基。如果你想在自己的程序中输出这样的文件，但不  
想使用GROMACS库，可以使用以下格式：__

__C 格式 "%5d%\-5s%5s%5d%8\.3f%8\.3f%8\.3f%8\.4f%8\.4f%8\.4f"__

__8\.7\. 文件格式 611__

__Fortran 格式 \(i5,2a5,i5,3f8\.3,3f8\.4\)__

__Pascal 格式留给用户做练习吧。__

__注意，这是用于输出的格式，如上面的示例所示，字段之间可能没有空格，因此无法使用相同格式的C  
语言语句进行读取。__

__hdb__

__hdb文件扩展名代表氢原子数据库。当使用 gmx pdb2gmx ↪ 297 程序构建原本就缺失的氢原子，或由\-ignh  
选项删除的氢原子时，需要这样一个文件。__

__itp__

__itp文件扩展名代表包含拓扑。这些文件可包含在拓扑文件中（扩展名为 top ↪ 617 ）。__

__log__

__日志文件由某些GROMACS程序生成，通常采用人类可读的格式。可以使用more logfile命令查看。__

__m2p__

__m2p文件格式包含用于 gmx xpm2ps ↪ 363 程序的输入选项。如果查看一下 gmx xpm2ps ↪ 363 给出的  
PostScript\(tm\)输出，就很容易理解所有的这些选项。__

__; Command line options of xpm2ps override the parameters in this file  
black&white =no ; Obsolete  
titlefont =Times\-Roman ; A PostScript Font  
titlefontsize = 20 ; Font size \(pt\)  
legend =yes ; Show the legend  
legendfont =Times\-Roman ; A PostScript Font  
legendlabel = ; Used when there is none in the\.xpm  
legend2label = ; Used when merging two xpm's  
legendfontsize = 14 ; Font size \(pt\)  
xbox =2\.0 ; x\-size of a matrix element  
ybox =2\.0 ; y\-size of a matrix element  
matrixspacing =20\.0 ; Space between 2 matrices  
xoffset =0\.0 ; Between matrix and bounding box  
yoffset =0\.0 ; Between matrix and bounding box  
x\-major = 20 ; Major ticks on x axis every\.\.frames  
x\-minor = 5 ; Id\.Minor ticks  
x\-firstmajor = 0 ; First frame for major tick  
x\-majorat0 =no ; Major tick at first frame  
x\-majorticklen =8\.0 ; x\-majorticklength  
x\-minorticklen =4\.0 ; x\-minorticklength  
x\-label = ; Used when there is none in the\.xpm  
x\-fontsize = 16 ; Font size \(pt\)  
x\-font =Times\-Roman ; A PostScript Font  
x\-tickfontsize = 10 ; Font size \(pt\)  
x\-tickfont =Helvetica ; A PostScript Font  
y\-major = 20  
y\-minor = 5  
y\-firstmajor = 0  
y\-majorat0 =no  
y\-majorticklen =8\.0  
y\-minorticklen =4\.0  
y\-label =  
y\-fontsize = 16  
y\-font =Times\-Roman  
y\-tickfontsize = 10  
y\-tickfont =Helvetica__

__map: 2019 版本__

__这类文件将矩阵数据映射到RGB值，用于 gmx do\_dssp ↪ 225 程序。__

__它的格式如下：第一行：指定颜色映射的元素数目。接下来的每一行：第一个字符为蛋白二级结构类型  
的编码。然后是用于绘图图例的字符串，然后是R（红色）G（绿色）和B（蓝色）值。__

__在下面的示例中，颜色为（按出现顺序）:白色，红色，黑色，青色，黄色，蓝色，品红色，橙色。__

__8  
~ Coil 1\.0 1\.0 1\.0  
E B\-Sheet 1\.0 0\.0 0\.0  
B B\-Bridge 0\.0 0\.0 0\.0  
S Bend 0\.0 0\.8 0\.8  
T Turn 1\.0 1\.0 0\.0  
H A\-Helix 0\.0 0\.0 1\.0  
G 3 \- Helix 1\.0 0\.0 1\.0  
I 5 \- Helix 1\.0 0\.6 0\.0__

__mdp__

__有关选项的详细说明，请参阅用户指南。__

__下面是一个示例mdp文件。选项的顺序并不重要，但如果同一选项输入了两次，会使用最后一次的设  
置（ gmx grompp ↪ 252 在覆盖前面的值时会给出注意信息）。等号左侧选项中的破折号和下划线没有区别。__

__示例选项的值用于模拟水盒子中的蛋白质，运行 1 纳秒MD。__

__注意：所选参数（如短程截断值）取决于所使用的力场。__

__integrator =md  
dt =0\.002  
nsteps = 500000__

__nstlog = 5000  
nstenergy = 5000  
nstxout\-compressed = 5000__

__continuation =yes  
constraints =all\-bonds  
constraint\-algorithm =lincs__

__cutoff\-scheme =Verlet__

__coulombtype =PME  
rcoulomb =1\.0__

__vdwtype =Cut\-off  
rvdw =1\.0  
DispCorr =EnerPres__

__tcoupl =V\-rescale  
tc\-grps =Protein SOL  
tau\-t =0\.1 0\.1  
ref\-t = 300 300__

__pcoupl =Parrinello\-Rahman  
tau\-p =2\.0  
compressibility =4\.5e\-5  
ref\-p =1\.0__

__使用此输入文件， gmx grompp ↪ 252 会生成一个包含注释的文件，默认名称为mdout\.mdp。这个文件会包  
含上述选项，以及未明确设置的所有其他选项，并给出了它们的默认值。__

__mtx__

__具有mtx扩展名的文件包含了矩阵。文件格式与 trr ↪ 619 格式相同。目前，这种文件格式仅用于Hessian  
矩阵，这种矩阵由 gmx mdrun ↪ 276 生成，并由 gmx nmeig ↪ 286 读取。__

__ndx__

__GROMACS索引文件（通常称为 index\.ndx）包含了一些用户可定义的原子集合。大多数分析程序，  
可视化程序（ gmx view ↪ 3562019 版本）和预处理器（ gmx grompp ↪ 252 ）都可以读取这种文件。如果没有提  
供索引文件，这些程序中的大多数都会创建默认的索引组，因此只有需要特殊组时才需要创建索引文件。__

__首先，将组的名称写在方括号之间。下面的原子编号可以延续任意多行。原子编号从 1 开始。__

__下面是一个示例文件：__

__\[ Oxygen \]  
1 4 7  
\[ Hydrogen \]  
2 3 5 6  
8 9__

__示例中有两个组，总共 9 个原子。第一个组Oxygen有 3 个原子。第二个组Hydrogen有 6 个原子。__

__可以使用 gmx make\_ndx ↪ 270 工具生成索引文件。__

__n2t__

__这种GROMACS文件可用于将结构文件中的原子名称初步转换为相应的原子类型。这主要用于 gmx  
x2top ↪ 361 程序，但用户应该知道，此文件中的信息非常有限。__

__下面是一个示例文件（share/top/gromos53a5\.ff/atomname2type\.n2t）:__

__H H 0\.408 1\.008 1 O 0\.1  
O OA \-0\.67415\.9994 2 C 0\.14H0\.1  
C CH3 0\.00015\.035 1 C 0\.15  
C CH0 0\.26612\.011 4 C 0\.15C0\.15 C0\.15 O0\.14__

__文件格式的简短说明如下：__

__第 1 列：原子的元素符号/原子名称中的第一个字符。__

__第 2 列：要指定的原子类型。__

__第 3 列：要指定的电荷。__

__第 4 列：原子的质量。__

__第 5 列：与该原子成键的其他原子的数目N。后面的字段数与此数字相关；对每个成键原子，指  
定其元素符号以及其键长的参考距离。__

__第 6 列以后：与待指定参数的原子（第 1 列）相连的N个连接（第 5 列）的元素符号和参考键长。  
参考键长与此文件中指定值的容差为\+/\- 10%。对超出此容差的任何键，程序都会将其识别为未  
与待指定参数的原子相连。__

__out__

__具有out扩展名的文件包含了通用的输出信息。由于无法对所有数据文件格式进行分类，GROMACS  
具有一种名为out的通用文件格式，没有限定任何格式。__

__pdb__

__具有 pdb ↪ 614 扩展名的文件为蛋白质数据库文件格式的分子结构文件。蛋白质数据库文件格式描述了  
一个分子结构中原子的位置。坐标来自 ATOM和 HETATM 记录，直到文件结束或遇到ENDMDL 记录。  
GROMACS程序可以读取和输出 CRYST1记录中模拟盒子的信息\.pdb格式也可以用作轨迹格式：可以  
读取一个文件中由ENDMDL分隔的几个结构，也可以用此格式输出多个结构。__

__示例__

__pdb文件应如下所示：__

__ATOM 1 H1 LYS 1 14\.260 6\.590 34\.480 1\.00 0\.00  
ATOM 2 H2 LYS 1 13\.760 5\.000 34\.340 1\.00 0\.00  
ATOM 3 N LYS 1 14\.090 5\.850 33\.800 1\.00 0\.00  
ATOM 4 H3 LYS 1 14\.920 5\.560 33\.270 1\.00 0\.00  
\.\.\.  
\.\.\.__

__rtp__

__rtp文件扩展名代表残基拓扑文件。 gmx pdb2gmx ↪ 297 需要这种文件来创建蛋白的GROMACS拓扑，蛋  
白一般包含在 pdb ↪ 614 文件中。这种文件包含了 4 种成键相互作用的默认相互作用类型以及残基条目，残  
基条目中包含了原子，以及可能的键，键角，二面角和反常二面角。可以为键，键角，二面角和反常二  
面角添加参数，这些参数会覆盖 itp ↪ 611 文件中的标准参数。这种做法只应该用于特殊情况。可以为每个  
成键相互作用添加字符串而不是参数，这个字符串会被复制到 top ↪ 617 文件中，GROMOS96力场就使用  
了这种方式。__

__gmx pdb2gmx ↪ 297 会自动生成所有的键角，这意味着 \[ angles \]字段仅用于覆盖 itp ↪ 611 参数。__

__gmx pdb2gmx ↪ 297 程序会自动为每个可旋转的键生成一个正常二面角，并倾向位于重原子上。当使用\[  
dihedrals \]字段时，不会为与指定二面角对应的键生成其他二面角。可以为一条可旋转的键指定一个  
以上的二面角。__

__gmx pdb2gmx ↪ 297 会将排除数设置为 3 ，这意味着最多 3 条键连接的原子之间的相互作用会被排除。程  
序会为相隔 3 条键的所有原子对生成配对相互作用（氢原子对除外）。当需要排除更多的相互作用，或  
不需要生成某些配对相互作用时，可以添加\[ exclusions \]字段，后面跟着位于不同行上的原子名称  
对。这些原子之间的所有非键和配对相互作用都将被排除。__

__下面是一个示例：__

__\[ bondedtypes \] ; mandatory  
; bonds angles dihedrals impropers  
1 1 1 2 ; mandatory__

__\[ GLY \] ; mandatory__

__\[ atoms \] ; mandatory  
; name type charge chargegroup  
N N \-0\.280 0  
H H 0\.280 0  
CA CH2 0\.000 1  
C C 0\.380 2  
O O \-0\.380 2__

__\[ bonds \] ; optional  
;atom1 atom2 b0 kb  
N H  
__

__N CA__

__CA C__

__C O__

__C N__

__\[ exclusions \] ; optional  
;atom1 atom2__

__\[ angles \] ; optional  
;atom1 atom2 atom3 th0 cth__

__\[ dihedrals \] ; optional  
;atom1 atom2 atom3 atom4 phi0 cp mult__

__\[ impropers \] ; optional  
;atom1 atom2 atom3 atom4 q0 cq  
N \-C CA H__

__C \-CA N \-O__

__\[ ZN \]  
\[ atoms \]  
ZN ZN 2\.000 0__

____r2b____

__r2b文件可以转换残基的残基名称，这些残基在不同力场中可能具有不同的名称，或者根据它们的质子  
化状态而具有不同的名称。__

____tdb____

__tdb文件包含了氨基酸末端的信息，这些末端可用于对多肽链进行封端。__

____tex____

__我们使用 __LaTeX__ 进行文档处理。虽然输入并不是那么用户友好，但与 word 相比有一些优势。__

____tng____

__具有\.tng 扩展名的文件可以包含与模拟轨迹相关的所有类型的数据。例如，它可能包含坐标，速度，  
力和/或能量。各种 mdp ↪ 612 文件选项可用于控制 gmx mdrun ↪ 276 输出哪些数据，输出数据是否压缩，以  
及压缩率多大。此文件采用便携式二进制格式，可以使用 gmx dump ↪ 227 读取。__

__gmx dump ↪ 227 \-f traj\.tng__

__或者，如果你的阅读速度不是很快，可以使用：__

__gmx dump\-f traj\.tng|less__

__你也可以使用以下方法快速查看文件内容（帧数等）:__

__gmx check ↪ 192 \-f traj\.tng__

__top__

__top文件扩展名代表拓扑。它是一个ascii文本文件， gmx grompp ↪ 252 可以读取这种文件，进行处理，并  
创建一个二进制拓扑（ tpr ↪ 619 文件）。__

__下面是一个示例文件：__

__;  
; Example topology file  
;  
\[ defaults \]  
; nbfunc comb\-rule gen\-pairs fudgeLJ fudgeQQ  
1 1 no 1\.0 1\.0__

__; The force field files to be included  
\#include "rt41c5\.itp"__

__\[ moleculetype \]  
; name nrexcl  
Urea 3__

__\[ atoms \]  
; nr type resnr residu atom cgnr charge  
1 C 1 UREA C1 1 0\.683  
2 O 1 UREA O2 1 \- 0\.683  
3 NT 1 UREA N3 2 \- 0\.622  
4 H 1 UREA H4 2 0\.346  
5 H 1 UREA H5 2 0\.276  
6 NT 1 UREA N6 3 \- 0\.622  
7 H 1 UREA H7 3 0\.346  
8 H 1 UREA H8 3 0\.276__

__\[ bonds \]  
; ai aj funct c0 c1  
3 4 1 1\.000000e\-013\.744680e\+05  
__

__3 5 1 1\.000000e\-013\.744680e\+05__

__6 7 1 1\.000000e\-013\.744680e\+05__

__6 8 1 1\.000000e\-013\.744680e\+05__

__1 2 1 1\.230000e\-015\.020800e\+05__

__1 3 1 1\.330000e\-013\.765600e\+05__

__1 6 1 1\.330000e\-013\.765600e\+05__

__\[ pairs \]  
; ai aj funct c0 c1  
2 4 1 0\.000000e\+000\.000000e\+00  
2 5 1 0\.000000e\+000\.000000e\+00  
2 7 1 0\.000000e\+000\.000000e\+00  
2 8 1 0\.000000e\+000\.000000e\+00  
3 7 1 0\.000000e\+000\.000000e\+00  
3 8 1 0\.000000e\+000\.000000e\+00  
4 6 1 0\.000000e\+000\.000000e\+00  
5 6 1 0\.000000e\+000\.000000e\+00__

__\[ angles \]  
; ai aj ak funct c0 c1  
1 3 4 1 1\.200000e\+022\.928800e\+02  
1 3 5 1 1\.200000e\+022\.928800e\+02  
4 3 5 1 1\.200000e\+023\.347200e\+02  
1 6 7 1 1\.200000e\+022\.928800e\+02  
1 6 8 1 1\.200000e\+022\.928800e\+02  
7 6 8 1 1\.200000e\+023\.347200e\+02  
2 1 3 1 1\.215000e\+025\.020800e\+02  
2 1 6 1 1\.215000e\+025\.020800e\+02  
3 1 6 1 1\.170000e\+025\.020800e\+02__

__\[ dihedrals \]  
; ai aj ak al funct c0 c1 c2  
2 1 3 4 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00  
6 1 3 4 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00  
2 1 3 5 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00  
6 1 3 5 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00  
2 1 6 7 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00  
3 1 6 7 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00  
2 1 6 8 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00  
3 1 6 8 1 1\.800000e\+023\.347200e\+01 2\.000000e\+00__

__\[ dihedrals \]  
; ai aj ak al funct c0 c1  
3 4 5 1 2 0\.000000e\+001\.673600e\+02  
6 7 8 1 2 0\.000000e\+001\.673600e\+02  
1 3 6 2 2 0\.000000e\+001\.673600e\+02__

__; Include SPC water topology  
\#include "spc\.itp"__

__\[ system \]  
Urea in Water__

__\[ molecules \]  
Urea 1  
SOL 1000__

__tpr__

__tpr文件扩展名代表便携式二进制运行输入文件。这类文件包含了模拟的初始结构，分子拓扑和所有的  
模拟参数。因为此文件为二进制格式，所以无法使用普通编辑器读取。要读取便携式二进制运行输入文  
件，可以使用：__

__gmx dump ↪ 227 \-s topol\.tpr__

__或者，如果你的阅读速度不是很快，可以使用：__

__gmx dump\-s topol\.tpr|less__

__你还可以使用以下方法比较两个tpr文件：__

__gmx check ↪ 192 \-s1 top1 \-s2 top2 | less__

__trr__

__具有trr扩展名的文件包含了模拟的轨迹。在这个文件中，包含了所有的坐标，速度，力和能量，输出  
方式由GROMACS的mdp文件决定。此文件为便携式二进制格式，可以使用 gmx dump ↪ 227 读取：__

__gmx dump\-f traj\.trr__

__或者，如果你的阅读速度不是很快，可以使用：__

__gmx dump\-f traj\.trr|less__

__你也可以使用以下方法快速查看文件内容（帧数等）:__

__gmx check ↪ 192 \-f traj\.trr__

__vsd__

__vsd文件包含了在一个力场中，如何为多个不同的分子设置虚拟位点的信息。__

__xdr__

__GROMACS使用XDR文件格式在内部存储坐标文件等内容。__

__xpm__

__GROMACS xpm文件格式与XPixMap格式兼容，用于存储矩阵数据。因此可以使用XV等程序直  
接查看GROMACS xpm文件。或者，也可以将其导入GIMP并缩放到300 DPI，对字体和图形使用  
强抗锯齿效果。xpm文件中的第一个矩阵数据文本行对应于矩阵的最后一行。除XPixMap格式外，  
GROMACS xpm文件可能包含额外的字段。当使用 gmx xpm2ps ↪ 363 将xpm文件转换为EPS文件时，  
会使用这些字段中的信息。可选的额外字段为：__

__在gv\_xpm声明之前：title，legend，x\-label,y\-label和type，这些字段后面都要跟着一  
个字符串。legend字段指定图例标题。type字段后面必须跟着"continuous"或"discrete"，  
它决定了在EPS文件中使用哪种类型的图例，默认为连续型。__

__xpm颜色映射条目后面可以跟着一个字符串，该字符串为相应颜色的标签。__

__在颜色映射和矩阵数据之间，可以出现x\-axis和/或y\-axis字段，它们指定相应轴的刻度标记。__

__下面的GROMACS xpm示例文件包含了所有额外字段。附加字段中的C注释分隔符和冒号是可选的。__

__/XPM/  
/This matrix is generated by g\_rms\./  
/title: "Backbone RMSD matrix"/  
/legend: "RMSD \(nm\)"/  
/x\-label:"Time \(ps\)"/  
/y\-label:"Time \(ps\)"/  
/type: "Continuous"/  
static chargv\_xpm\[\]=\{  
"13 13 6 1",  
"A c \#FFFFFF"/" 0 "/,  
"B c \#CCCCCC"/"0\.0399"/,  
"C c \#999999"/"0\.0798"/,  
"D c \#666666"/"0\.12"/,  
"E c \#333333"/"0\.16"/,  
"F c \#000000"/"0\.2"/,  
/x\-axis: 04080120160200240280320360400440480 /  
/y\-axis: 04080120160200240280320360400440480 \*/  
"FEDDDDCCCCCBA",  
"FEDDDCCCCBBAB",  
"FEDDDCCCCBABC",  
"FDDDDCCCCABBC",  
"EDDCCCCBACCCC",  
"EDCCCCBABCCCC",  
"EDCCCBABCCCCC",  
"EDCCBABCCCCCD",  
"EDCCABCCCDDDD",  
"ECCACCCCCDDDD",  
"ECACCCCCDDDDD",  
"DACCDDDDDDEEE",  
"ADEEEEEEEFFFF"__

__xtc__

__xtc格式为轨迹的便携式格式。它使用 xdr 例程来读写数据，这些数据是为Unix NFS系统创建的。输  
出轨迹时使用了精度降低的算法，该算法工作方式如下：坐标（以nm为单位）乘上一个缩放因子，通  
常为 1000 ，因此得到的坐标以pm为单位。将得到的值四舍五入为整数值。然后使用其他一些技巧，例  
如，在序列中的接近的原子通常也会在空间上接近（如水分子）。为此，对 xdr 库进行了扩展，添加了一  
个特殊的例程来编写3\-D浮点坐标。该例程最初由Frans van Hoesel编写，作为Europort项目的一部  
分。它的更新版本可以通过 此链接↪https://github\.com/Pappulab/xdrf获得。__

__所有数据都使用对 xdr 例程的调用来存储。具体格式如下：__

__int magic 整数一个神奇的数字，对于当前的文件版本，其值为 1995 。__

__int natoms 整数轨迹中的原子数。__

__int step 整数模拟步数。__

__float time 浮点数模拟时间。__

__float box\[3\]\[3\] 浮点数模拟盒子存储为三个基向量的集合，以便可以用于三斜PBC。对于长方体盒子，  
盒子边长存储在矩阵的对角线上。__

__3dfcoord x\[natoms\] 坐标本身以较低的精度存储。请注意，当原子数小于 9 时，不会使用降低精度的  
算法。__

__在 C\+\+ 程序中使用 xtc__

__可以自己编写分析工具以利用压缩的\.xtc格式文件：请参阅安装的share/gromacs/template目  
录中的示例文件template\.cpp，以及https://manual\.gromacs\.org/current/doxygen/html\-full/page\_  
analysistemplate\.xhtml文档。__

__要读写xtc文件,可使用xtcio\.h中的下列子程序:__

__/All functions return 1 if successful, 0 otherwise/__

__struct t\_fileioopen\_xtc\(const charfilename, const charmode\);  
/Open a file for xdr I/O\*/__

__void close\_xtc\(struct t\_fileiofio\);  
/Close the file for xdr I/O\*/__

__intread\_first\_xtc\(struct t\_fileiofio,  
int natoms,  
int64\_t\* step,  
real\* time,  
matrix box,  
rvec\*\* x,  
real\* prec,  
gmx\_bool\* bOK\);  
/Open xtc file, read xtc file first time, allocate memory for x/__

__intread\_next\_xtc\(struct t\_fileiofio,intnatoms, int64\_tstep, realtime, matrix box,␣  
↪rvecx, realprec, gmx\_boolbOK\);  
/Read subsequent frames/__

__intwrite\_xtc\(struct t\_fileiofio,intnatoms, int64\_t step, real time, const rvecbox,␣  
↪const rvecx, real prec\);  
/Write a frame to xtc file\*/__

__要使用库函数,可以将"gromacs/fileio/xtcio\.h"包含在你的文件中,并链接\-lgromacs\.__

__在 C 程序中使用 xtc: 2019 版本__

__要读写这些文件，可以使用以下C例程：__

__/All functions return 1 if successful, 0 otherwise/__

__externintopen\_xtc\(XDRxd,charfilename,charmode\);  
/Open a file for xdr I/O\*/__

__extern void close\_xtc\(XDRxd\);  
/Close the file for xdr I/O\*/__

__externintread\_first\_xtc\(XDRxd,charfilename,  
intnatoms,intstep,realtime,  
matrix box,rvecx,realprec\);  
/Open xtc file, read xtc file first time, allocate memory for x/__

__externintread\_next\_xtc\(XDRxd,  
intnatoms,intstep,realtime,  
matrix box,rvecx,realprec\);  
/Read subsequent frames/__

__externintwrite\_xtc\(XDRxd,  
intnatoms,intstep,real time,  
matrix box,rvecx,real prec\);  
/Write a frame to xtc file/__

__要使用库函数，请在文件中包含"gromacs/fileio/xtcio\.h"，并在链接时指定\-lgmx\.$\(CPU\)。__

__检测到处于定义的划分圆柱内部时，才能认为离子通过了特定通道。如果 swap\-frequency太高，特__

__定的离子可能在一个交换步骤中被检测到处于腔室 A ，在下一交换步骤中却被检测到处于腔室 B ，因此__

__就无法清楚地确定离子到底是通过了哪个通道。__

__用于CompEL模拟的双层系统可以很容易地使用下述方法创建：利用 gmx editconf ↪ 231 \-translate 0 0__

__<l\_z>命令在膜的法线方向\(通常为𝑧\)上重复现有的膜/通道MD系统，其中l\_z为重复方向的盒子__

__长度。如果已经为单层系统的通道定义了索引组，那么使用 gmx make\_ndx ↪ 270 \-n index\.ndx \-twin就__

__可以得到双层系统的索引组。__

__为抑制膜沿交换方向的大幅波动，采用伞形牵引（见牵引代码↪ 626 一节）在每个通道和/或双层中心之间__

__施加简谐势（仅作用于交换维度）可能会有帮助。__

__多重通道__

__如果划分组包含的分子数大于 1 ，必须选择所有分子相互之间的正确的PBC映像，这样才能正确地确__

__定通道中心。GROMACS假设 tpr ↪ 619 文件中初始结构的PBC表示是正确的。设置下面的环境变量可检__

__查情况是否如此：__

__GMX\_COMPELDUMP:将完整化后的初始结构输出到 pdb ↪ 614 文件。__

#### 8\.8\.9 使用自由能代码计算 PMF

##### 自由能耦合参数方法（参见自由能计算↪ 514 一节）提供了几种计算平均力势的方法。通过使用简谐势或

##### 约束连接两个原子，可以计算它们之间的平均力势。为此，有一些特殊的势能函数可以避免产生额外的

__排除，参见排除↪ 580 一节。当状态B中的最小位置或约束长度比状态A中的大1 nm时，限制力或约束  
力为𝜕𝐻/𝜕𝜆。通过设置 mdp ↪ 612 文件中的 delta\-lambda可以改变原子间的距离，它是𝜆和时间的函  
数。得到的结果应当与使用牵引代码中的伞形采样和约束牵引所得的结果完全相同（尽管由于实现方法  
不同在数值上不可能完全相同）。与牵引代码不同，自由能代码也可以处理通过约束连接的原子。  
也可以利用位置限制来计算平均力势。采用位置限制时，原子通过简谐势连接到空间中的某一位置  
（参见位置限制↪ 541 一节）。这些位置可以作为耦合参数𝜆的函数。A状态和B状态的位置可分别利  
用 grompp ↪ 252 的\-r和\-rb选项进行设置。可以使用这种方法进行靶向MD;注意，我们并不鼓励对蛋  
白质使用靶向MD。将这些构象作为状态A和B的位置限制坐标，就可以迫使蛋白质从一种构象转变  
到另一种构象。然后可以从 0 到 1 缓慢地改变𝜆的值。这种方法的主要缺点在于，蛋白质的构象自由度  
受到位置限制的严重制约，而与从状态A到B状态的变化无关。此外，蛋白质由状态A到状态B的强  
制转变几乎处于一条直线上，而真实的路径可能大不相同。更适合这种方法的一个例子是固体系统或限  
制于墙之间的液体。对这种系统，你可能想要测量改变到边界或墙之间的距离时所需要的力。由于边界  
（或墙）已经需要固定，因此位置限制并不会限制系统的采样。__

####  VMD 插件用于轨迹文件输入 / 输出

__GROMACS工具可以使用已经安装的 VMD↪http://www\.ks\.uiuc\.edu/Research/vmd/ 插件来读写非GROMACS  
原生格式的轨迹文件。例如，你可以直接将AMBER DCD格式的轨迹文件提供给GROMACS工具。__

__要使用这个功能，VMD的版本不能低于1\.8，还需要你的系统提供dlopen函数，这样程序运行时才能  
够确定存在哪些插件，以及构建GROMACS时构建了共享库。CMake会在你的路径下查找vmd可执  
行文件，根据查找到的路径，或者在配置或运行时的环境变量VMDDIR来定位插件。或者，运行时可使  
用VMD\_PLUGIN\_PATH 来指定插件的路径。请注意，这些插件是二进制格式的，必须与其所在机器的架  
构匹配。__

## 第 9 章NBLIB API

### 9\.1 模拟 MD 程序编写指南

##### NB\-LIB的目标是使研究人员能够以编程方式定义分子模拟。传统上，这是通过使用一堆可执行文件以

##### 及手动的工作流程，再由”黑箱”的模拟引擎来完成的。NB\-LIB支持用户在更细的层次上编写各种新的

##### 模拟和分析工作流程。

##### NB\-LIB所具有的灵活性使得许多应用案例成为可能。这包括自定义更新规则、定义定制的力或协调一

##### 组模拟。NB\-LIB还支持编写传统的MD模拟和分析。

##### 本文介绍使用NB\-LIB的API编写MD程序的步骤，这些API暴露了GROMACS软件包的部分功能。

#### 9\.1\.1 全局定义

##### NB\-LIB程序是用 须包含其用于I/O或高级任务的头文件。此外，还必须包含

__NB\-LIB暴露的各 可以直接复制下面的代码。最后，我们使用命名空间nblib来  
定义库中的数据结 使得每次使用函数或数据结构时可以忽略nblib指定符。__

__\#include__

__\#include"nblib/box\.h"  
\#include"nblib/forcecalculator\.h"  
\#include"nblib/integrator\.h"  
\#include"nblib/molecules\.h"  
\#include"nblib/nbkerneloptions\.h"  
\#include"nblib/particletype\.h"  
\#include"nblib/simulationstate\.h"__

__\#include"nblib/topology\.h"__

__usingnamespacenblib ;__

#### 9\.1\.2 定义粒子数据

__// 参数来自 GROMOS 兼容的 2016H66 力场__

__structOWaterAtom  
\{  
ParticleName name="Ow";  
Mass mass=15\.999;  
C6 c6 =0\.0026173456;  
C12 c12 =2\.634129e\-06;  
\};__

__structHwAtom  
\{  
ParticleName name="Hw";  
Mass mass=1\.00784;  
C6 c6 =0\.0;  
C12 c12 =0\.0;  
\};__

__structCMethAtom  
\{  
ParticleName name="Cm";  
Mass mass=12\.0107;  
C6 c6 =0\.01317904;  
C12 c12 =34\.363044e\-06;  
\};__

__structHcAtom  
\{  
ParticleName name="Hc";  
Mass mass=1\.00784;  
C6 c6 =8\.464e\-05;  
C12 c12 =15\.129e\-09;  
\};__

__体系中有多少种粒子类型就可以有多少种这样的结构。严格来说，这样组织数据并不是必须的，这里只是  
为了清晰起见。如上所示，多个粒子可以对应同一个元素，因为原子质量可以因分子环境而变化。例如，羧  
基中的碳原子与甲基中的碳原子会有不同的参数。我们可以从任何标准力场中获得参数集，或者生成新  
的参数来研究新的化合物或力场__

#### 9\.1\.3 定义坐标、速度和力缓冲区

__std::vector<gmx::RVec>coordinates=\{  
\{0\.794,1\.439,0\.610\}, \{1\.397,0\.673,1\.916\},\{0\.659,1\.080,0\.573\},  
\{1\.105,0\.090,3\.431\}, \{1\.741,1\.291,3\.432\},\{1\.936,1\.441,5\.873\},  
\{0\.960,2\.246,1\.659\}, \{0\.382,3\.023,2\.793\},\{0\.053,4\.857,4\.242\},  
\{2\.655,5\.057,2\.211\}, \{4\.114,0\.737,0\.614\},\{5\.977,5\.104,5\.217\},  
\};__

__std::vector<gmx::RVec>velocities=\{  
\{0\.0055,\-0\.1400,0\.2127\},\{0\.0930,\-0\.0160,\-0\.0086\}, \{0\.1678,0\.2476,\-0\.0660\},  
\{0\.1591,\-0\.0934,\-0\.0835\},\{\-0\.0317,0\.0573,0\.1453\}, \{0\.0597,0\.0013,\-0\.0462\},  
\{0\.0484,\-0\.0357,0\.0168\},\{0\.0530,0\.0295,\-0\.2694\},\{\-0\.0550,\-0\.0896,0\.0494\},  
\{\-0\.0799,\-0\.2534,\-0\.0079\},\{0\.0436,\-0\.1557,0\.1849\},\{\-0\.0214,0\.0446,0\.0758\},  
\};__

__std::vector<gmx::RVec>forces=\{  
\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},  
\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},  
\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},  
\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},\{0\.0000,0\.0000,0\.0000\},  
\};__

__我们可以使用gmx::RVec的std::vector来初始化粒子的坐标，这是一种特定的数据类型，用于保存三  
维向量。见 RVec的Doxygen页面↪\.\./doxygen/html\-lib/namespacegmx\.xhtml\#a139c1919a9680de4ad1450f42e37d33b\.__

#### 9\.1\.4 编写 MD 程序

__与任何基本的C\+\+程序一样，需要有一个main\(\)函数。__

__定义粒子类型__

__int main\(\)  
\{  
// 引入参数结构  
OwAtom owAtom;  
HwAtom hwAtom;  
CMethAtom cmethAtom;  
HcAtom hcAtom;__

__// 创建粒子__

__ParticleTypeOw\(owAtom\.name,owAtom\.mass\);__

__ParticleTypeHw\(hwAtom\.name,hwAtom\.mass\);__

__ParticleTypeCm\(cmethAtom\.name,cmethAtom\.mass\);__

__ParticleTypeHc\(hcAtom\.name,hcAtom\.mass\);__

__与之前一样，定义ParticleType数据的辅助结构并不严格需要，这里展示只是为了清晰起见，__

__有ParticleType CMethAtom\(ParticleName\("Cm"\), Mass\(12\.0107\)\);这一行就足够了。__

定义非键相互作用

__ParticleTypeInteractionsinteractions\(CombinationRule::Geometric\);__

__// 为粒子类型添加非键相互作用  
interactions\.add\(owAtom\.name,owAtom\.c6,owAtom\.c12\);  
interactions\.add\(hwAtom\.name,hwAtom\.c6,hwAtom\.c12\);  
interactions\.add\(cmethAtom\.name,cmethAtom\.c6,cmethAtom\.c12\);  
interactions\.add\(hcAtom\.name,hcAtom\.c6,hcAtom\.c12\);__

__对 于 Lennard\-Jones 相 互 作 用， 我 们 定 义 了 一 个 sphinxcodeParticleTypeInteractions 对 象。  
每 个ParticleType的 粒 子 都 基 于C6 和 C12参 数 相 互 作 用。 两 种 不 同 粒 子 的 参 数 使  
用Geometric 或 LorentzBerthelot 组合规则CombinationRule进行平均。更多细节见这里↪http:  
//manual\.gromacs\.org/documentation/2019/reference\-manual/functions/nonbonded\-interactions\.html\#the\-lennard\-jones\-interaction。默认选  
择CombinationRule::Geometric。__

__我们将每种粒子类型的相互作用参数添加到ParticleTypeInteractions对象中。结果是  
一个表格，其中包含为所有ParticleType对之间指定的相互作用。下面的矩阵说明了使  
用CombinationRule::Geometric创建的成对C6参数。__

__\# Ow Hw Cm Hc__

__Ow 0\.0026 0\.0 0\.42 4\.7e\-4__

__Hw 0\.0 0\.0 0\.0 0\.0__

__Cm 0\.42 0\.0 0\.013 1\.05e\-3__

__Hc 4\.7e\-4 0\.0 1\.05e\-3 8\.5e\-5__

__对于某一特定的相互作用对，用户也可以使用自定义参数覆盖指定的CombinationRule。下面的重载会  
取代根据Ow和Cm粒子类型之间的CombinationRule计算出来的参数。__

__interactions\.add\("Ow","Cm",0\.42,42e\-6\);__

__为了方便模块化、代码可复用，可以将多个ParticleTypeInteractions对象组合起来。假定我们已经  
定义了otherInteractions，就可以用interactions\.merge\(otherInteractions\)进行组合。__

##### 定义分子

__Moleculewater\("Water"\);  
Moleculemethane\("Methane"\);__

__water\.addParticle\(ParticleName\("O"\),Ow\);  
water\.addParticle\(ParticleName\("H1"\),Hw\);  
water\.addParticle\(ParticleName\("H2"\),Hw\);__

__water\.addExclusion\("H1","O"\);  
water\.addExclusion\("H2","O"\);__

__methane\.addParticle\(ParticleName\("C"\), Cm\);  
methane\.addParticle\(ParticleName\("H1"\),Hc\);  
methane\.addParticle\(ParticleName\("H2"\),Hc\);  
methane\.addParticle\(ParticleName\("H3"\),Hc\);  
methane\.addParticle\(ParticleName\("H4"\),Hc\);__

__methane\.addExclusion\("H1","C"\);  
methane\.addExclusion\("H2","C"\);  
methane\.addExclusion\("H3","C"\);  
methane\.addExclusion\("H4","C"\);__

__我们开始使用分子的组成粒子来声明分子。一个字符串标识符必须唯一地识别为分子中的一个特定粒子。  
也可以为每个粒子定义部分电荷，用于计算库仑相互作用。__

__water\.addParticle\(ParticleName\("O"\),Charge\(\-0\.04\), Ow\);__

__添加排除项可以确保只在必要时才计算非键相互作用。例如，如果两个粒子共享一条键，键的势能会使  
得非键项可以忽略不计。粒子自身的排除默认启用。我们基于在addParticle\(\)过程中指定的唯一标识  
符以及此后列出的相互作用添加排除项。__

__定义列表相互作用__

__在一个分子内可以定义其组成粒子之间的键、角和二面角等相互作用。NB\-LIB提供了几个常用的 2 、 3__

__和 4 中心相互作用的具体实现。__

__HarmonicBondTypeohHarmonicBond\( 1 , 1 \);  
HarmonicBondTypehcHarmonicBond\( 2 , 1 \);__

__DefaultAnglehohAngle\(Degrees\( 120 \), 1 \);  
DefaultAnglehchAngle\(Degrees\(109\.5\), 1 \);__

__// 添加水的简谐键  
water\.addInteraction\("O","H1",ohHarmonicBond\);  
water\.addInteraction\("O","H2",ohHarmonicBond\);__

__// 添加水的键角  
water\.addInteraction\("H1","O","H2",hohAngle\);__

__// 添加甲烷的简谐键  
methane\.addInteraction\("H1","C",hcHarmonicBond\);  
methane\.addInteraction\("H2","C",hcHarmonicBond\);  
methane\.addInteraction\("H3","C",hcHarmonicBond\);  
methane\.addInteraction\("H4","C",hhcHarmonicBondc\);__

__// 添加甲烷的键角  
methane\.addInteraction\("H1","C","H2",hchAngle\);  
methane\.addInteraction\("H1","C","H3",hchAngle\);  
methane\.addInteraction\("H1","C","H4",hchAngle\);  
methane\.addInteraction\("H2","C","H3",hchAngle\);  
methane\.addInteraction\("H2","C","H4",hchAngle\);  
methane\.addInteraction\("H3","C","H4",hchAngle\);__

__定义模拟和非键计算的选项__

__// 定义模拟盒子  
Boxbox\(6\.05449\);__

__// 定义非键内核的选项  
NBKernelOptionsoptions;__

__可以使用一个参数定义正方体盒子，也可以使用 3 个分别指定长宽高的参数来定义盒子。__

__NBKernelOptions包含一组标识和配置选项，用于硬件环境和模拟的相关计算。下表给出了可以设置的  
可能选项。__

__定义拓扑和模拟状态__

__我们使用TopologyBuilder 类建立体系的拓扑，并使用其公共函数添加之前定义的Molecule对象以  
及ParticleTypesInteractions。我们使用buildTopology\(\)函数得到实际的Topology对象，包括所  
有的排除、相互作用图,基于定义的实体构建的列表相互作用数据。__

__TopologyBuildertopologyBuilder;__

__// 添加分子  
topologyBuilder\.addMolecule\(water, 10 \);  
topologyBuilder\.addMolecule\(methane, 10 \);__

__// 添加非键相互作用图  
topologyBuilder\.addParticleTypesInteractions\(interactions\);__

__Topologytopology=topologyBuilder\.buildTopology\(\);__

__我们现在有了所有需要的东西，可以使用SimulationState对象完全描述我们的体系。这是使用拓扑、  
盒子、粒子坐标和速度建立的。这个对象作为体系的快照，可用于分析或从已知状态开始模拟。__

__SimulationStatesimulationState\(coordinates,velocities,forces,box,topology\);__

__编写 MD 循环__

__现在我们已经完全描述了我们的体系和问题，我们需要两个实体来编写 MD循环。第一个__

__是ForceCalculator，第二个是积分器。NB\-LIB自带了一个LeapFrog积分器，但用户也可以编写  
自定义的积分器。__

__// 力计算器包含了计算力所需的所有数据  
ForceCalculatorforceCalculator\(simulationState,options\);__

__// 积分需要质量、位置和力  
LeapFrogintegrator\(simulationState\);__

__// 分配一个力的缓冲区  
gmx::ArrayRef<gmx::RVec>userForces\(topology\.numParticles\(\)\);__

__// MD 循环  
int numSteps= 100 ;__

__for \(i= 0 ;i<numSteps;i\+\+\)  
\{  
userForces=forceCalculator\.compute\(\);__

__// 这些力不会自动更新，以便用户可以添加自定义的力。__

__std::copy\(userForces\.begin\(\),userForces\.end\(\),begin\(simulationState\.forces\(\)\)\);__

__// 以 1 fs 的时间步长进行积分__

__integrator\.integrate\(1\.0\);__

__\}__

__return 0 ;  
\} // main 主函数__

### 9\.2 为 NB\-lIB 添加新的列表相互作用

##### 目前，NB\-LIB的代码路径可以处理两个、三个、四个和五个不同粒子之间的相互作用。通过修改以下

##### 三个文件，可以很容易地扩展NB\-LIB以支持新的粒子相互作用形式。

##### 两中心相互作用必须使用中心之间的距离作为力计算内核的输入。三中心相互作用的形式为

__\(particleI, particleJ, ParticleK\)。在这种情况下，中间的粒子 particleJ 会作为计算角度  
时的中心。此角度必须作为三中心力计算内核的输入。同样，对于四中心相互作用，二面角phi必须作  
为力计算内核的输入。满足这些限制后，就可以修改以下三个文件来添加新的计算内核。__

__1\) bondtypes\.h__

__2\) definitions\.h__

__3\) kernels\.hpp__

####  bondtypes\.h

__该文件包含了每种相互作用类型参数集的结构体struct。新相互作用类型要作为单独的结构体添加到  
这里。对内容没有要求，但为方便起见，可以使用现有的 NAMED\_MEBERS宏，并继承std::tuple或  
std::array。宏可以用于定义相应设置器和获取器的参数名。例如，NAMED\_MEMBERS\(forceConstant,  
equilDistance\)会展开为__

__inlineauto &forceConstant\(\)\{ return std::get< 0 >\(\* this \);\}  
inlineauto &equilDistance\(\)\{ return std::get< 1 >\(\* this \);\}  
inlineconstauto &forceConstant\(\) const \{ return std::get< 0 >\(\* this \); \}  
inlineconstauto &equilDistance\(\) const \{ return std::get< 1 >\(\* this \); \}__

__将所有的放在一起,我们就可以为新相互作用类型定义完整的参数集,如下:__

__\_/\*\! \\brief new bond type__

__V\(r; forceConstant, equilDistance, scaleFactor\)__

__= forceConstant \* exp\( \(r \- equilDistance\) / scaleFactor\)  
\*/\_  
__structNewBondType__ : __public__ std::tuple<real,real, __int__ >  
\{  
NewBondType\(\)= __default__ ;  
NewBondType\(ForceConstantf,EquilDistanced,ScaleFactors\):  
std::tuple<real,real, __int__ >\{f,d,s\}  
\{  
\}__

__NAMED\_MEMBERS\(forceConstant,equilDistance,scaleFactor\)  
\};__

#### definitions\.h

##### 该文件的开头是预处理宏列表，用以将具体的相互作用类型分为二中心、三中心、四中心和五中心类

##### 型。要添加新的相互作用类型，用户必须将其参数结构体名称添加到相应中心数的宏中。在本例中，

__NewBondType为一个二中心相互作用,因此要将其添加到SUPPORTED\_TWO\_CENTER\_TYPES宏中。假定唯  
一的其余二中心相互作用被称为DefaultBond，结果将如下面的代码片段所示。__

__\#define SUPPORTED\_TWO\_CENTER\_TYPES DefaultBond, NewBondType__

__在这个宏中添加NewBondType可以确保NBLIBmolecule 类的addInteraction函数支持添加新的  
键类型，并将其包含在topology类提供的列表相互作用数据中。__

__需要注意的是，从C\+\+17开始，除了预处理器宏（preprocessor macro）之外，没有其他方法可以通过  
上述宏来添加所需的模板实例。在NBLIB中，我们的设计初衷是，我们不想在用户头文件中公开模板  
化的接口，正是出于这个原因，我们明确地需要用这个宏中定义的所有支持的列表相互作用类型来实例  
化接口。__

####  kernels\.hpp

##### 在这个文件中，需要实现每种相互作用类型的实际的力计算内核。每个内核调用都是模板化的，允许各

__种精度，并通过重载bondKernel来访问,可以从const NewBondType&参数中提取相关参数。内核的  
返回类型始终是力和势的std::tuple。__

__/\*\! \\brief kernel to calculate the new bond type force__

__\*__

__\* \\param k Force constant__

__\* \\param x0 Equilibrium distance__

__\* \\param scale The scaling factor__

__\* \\param x Input bond length__

__\*__

__\* \\return tuple<force, potential energy>__

__\*/__

__template < classT >__

__std::tuple<T, T>newBondForce\(Tk,Tx0,Tscale,Tx\)__

__\{__

__realexponent=std::exp\(\(x\-x0\)/scale\);__

__realepot=k\*exponent;__

__realforce= epot/scale;__

__return std::make\_tuple\(force,epot\);__

__\}__

__template < classT >  
inlineauto bondKernel\(T dr, const NewBondType&bond\)  
\{__

__return newBondForce\(bond\.forceConstant\(\),bond\.equilDistance\(\),bond\.scaleFactor\(\),dr\);__

__\}__

### 9\.3 NB\-LIB 中成键力数据格式的设计目标和动机

##### GROMACS中列表力的当前格式如下:

__structInteractionDefinitions__

__\{__

__std::vector<t\_iparams>iparams;__

__std::array<std::vector< int >,F\_NRE>il;__

__\};__

__该格式涵盖所有相互作用类型，即t\_iparams是一个联合体类型，可以容纳任何类型的参数。另一个名  
为il 的成员包含每种相互作用类型的索引，其中F\_NRE为GROMACS支持的相互作用类型的数目。  
更准确地说，il的每个成员 std::vector都是一个给定相互作用类型的所有相互作用的扁平化  
列表。该向量包含每个相互作用的N\+1个整数索引，其中N为相互作用所涉及的粒子数。还需要一个  
额外的索引来获取iparams中正确的参数，因此每种相互作用的索引总数为N\+1。  
将所有类型存储在联合体数据类型中的最大优势（曾经）是，可以使用简单的for循环对所有类型进行  
遍历。在C\+\+11之前，甚至可能是在C\+\+14之前，对不同类型进行循环是一件非常麻烦的事情，而联  
合体数据类型方法很可能是实践中唯一可行的解决方案。然而，这种方法的一个缺点是，如果只有单个  
（联合体）类型，就无法利用编译器的类型系统，其中最重要的是静态分支，例如重载解析。因此，只能  
使用if语句进行动态分支。  
举例来说，考虑一下GROMACS中顶层calc\_listed\(const InteractionDefinitions& idef, \.\.\.\)  
的实现，其实质是这样的：__

__void calc\_listed\( const InteractionDefinitions&idef,\.\.\.\)__

__\{__

__// manage timing and multi\-threading__

__for \( int ftype= 0 ;ftype<F\_NRE;\+\+type\)__

__\{__

__// branch out and descend stack for 2 intermediate functions based on__

__// the type of interaction that ftype corresponds to__

__// then call a function from a pointer table__

__bondFunction\*bonded=bondedInteractionFunctions\[ftype\];__

__// compute all forces for ftype__

__bonded\(idef\.iparams,idef\.il\[ftype\],\.\.\.\);__

__\}__

__// reduce thread output__

__\}__

__GROMACS支持大量不同的列表相互作用类型，如不同类型的键、角、正常二面角和反常二面角。这些__

##### 不同类型需要不同的处理方法，最后从函数指针表中选择正确的力内核。处理代码需要正确地分支所有

##### 不同情况,这导致调用栈相当深,大量分支逻辑，并最终占整体复杂度的相当大部分，而在理想情况下，

##### 应该只包括特定类型的力计算实现。

### 9\.4 列表力的类型感知方法

##### NB\-LIB采用类型感知数据格式，将每种相互作用类型作为一个单独的（C\+\+）类型来实现，旨在降低

##### 代码的整体复杂度。给定相互作用类型的格式如下：

__template < classInteraction >  
structInteractionData  
\{  
std::vector<Index>indices;  
std::vector parameters;  
\};__

__对于每种相互作用类型，我们都会存储相互作用索引和相互作用参数。虽然（C\+\+）类型不同，但实际  
存储的数据完全相同：每个N中心相互作用需要N\+1个整数索引,外加唯一参数。Interaction的一  
个例子是HarmonicBond，它的公共部分看起来像这样：__

__classHarmonicBond  
\{  
public :  
// return lvalue ref for use with std::tie  
// in order to leverage std::tuple comparison ops  
const real&forceConstant\(\);  
const real&equilDistance\(\);  
\};__

__Index特征类推导出了std::array<int, 3>，因为对于每个简谐键，我们都需要两个int来表示坐  
标索引，第三个int来查找parameters向量中的键参数。对于角和二面角，Index特征会额外增加  
一个或两个int来保存额外的坐标索引。__

__最后，我们将所有类型的相互作用收集到一个 std::tuple中，这样NB\-LIB中列表力的完整定义看起  
来如下：__

__using ListedInteractions=std::tuple<InteractionData,\.\.\.,InteractionData  
↪,\.\.\.>;__

__ListedInteractions的一个重要特性是，它存储的信息与InteractionDefinitions完全相同，因此  
双方之间的转换很容易实现。__

### 9\.5 NB\-LIB 列表力管线

##### 根据上述格式提供的列表相互作用数据，计算相应力所需的步骤简述如下：

##### • 循环所有相互作用类型

##### • 循环给定类型的所有相互作用

##### • 调用相互作用类型内核,存储力并返回能量

##### 这个流程与GROMACS的当前实现完全一样\.在实际代码中,第一步类似:

__template < classBuffer , classPbc >  
auto reduceListedForces\( const ListedInteractions&interactions,  
const std::vector<gmx::RVec>&x,  
Buffer\*forces,  
const Pbc&pbc\)  
\{  
std::array<real,std::tuple\_size::value>energies;__

__// lambda function, will be applied to each type__

__auto computeForceType=\[forces,&x,&energies,&pbc\]\( constauto &ielem\)\{__

__realenergy=computeForces\(ielem\.indices,ielem\.parameters,x,forces,pbc\);__

__energies\[FindIndex<std::decay\_t< decltype \(ilem\)>,ListedInteractions>\{\}\]=energy;__

__\};__

__// apply the lambda to all bond types__

__for\_each\_tuple\(computeForceType,interactions\);__

____return__ energies;  
\}__

__借助通用lambda和C\+\+17单行for\_each\_tuple 中的 std::apply ，我们可以毫不费力地为元  
组中的不同类型生成循环。虽然 reduceListedForces 实现了对相互作用类型的循环，但下一层  
computeForces实现了对给定类型的所有相互作用的循环：__

__template < classIndex , classInteractionType , classBuffer , classPbc >  
realcomputeForces\( const std::vector&indices,  
const std::vector&iParams,  
const std::vector<gmx::RVec>&x,  
Buffer\*forces,  
const Pbc&pbc\)  
\{  
realEpot=0\.0;__

__for \( constauto &index:indices\)__

__\{__

__Epot\+=dispatchInteraction\(index,iParams,x,forces\);__

__\}__

__return Epot;  
\}__

##### 在联合体数据类型方法中，需要对所有相互作用类型手动实现此循环，而在NB\-LIB中，只需实现一次

##### 即可。

##### 现在，我们已经深入到单个键、角和二面角的层面。此时，接下来的步骤取决于相互作用的实际类型。

##### 但我们现在还没有将每个简谐键、立方键、简谐角等分派到它们各自的路径上，而是根据相互作用中心

__的数目进行区分。通过重载解析，会调用dispatchInteraction的相应版本，比如这个版本就是针对  
二中心相互作用的：__

__template < classBuffer , classTwoCenterType , classPbc >  
std::enable\_if\_t<IsTwoCenter::value,real>  
dispatchInteraction\( const InteractionIndex&index,  
const std::vector&bondInstances,  
const std::vector<gmx::RVec>&x,  
Buffer\*forces,  
const Pbc&pbc\)  
\{  
int i=std::get< 0 >\(index\);  
int j=std::get< 1 >\(index\);  
const gmx::RVec&x1=x\[i\];  
const gmx::RVec&x2=x\[j\];  
const TwoCenterType&bond=bondInstances\[std::get< 2 >\(index\)\];__

__gmx::RVecdx;__

__// calculate x1 \- x2 modulo pbc__

__pbc\.dxAiuc\(x1,x2,dx\);__

__realdr2=dot\(dx,dx\);__

__realdr =std::sqrt\(dr2\);__

__auto \[force,energy\]=bondKernel\(dr,bond\);__

__// avoid division by 0__

__if \(dr2\!=0\.0\)__

__\{__

__force/=dr;__

__detail::spreadTwoCenterForces\(force,dx,&\(\*forces\)\[i\],&\(\*forces\)\[j\]\);__

__\}__

____return__ energy;  
\}__

__我们可以再次观察到，不同的二中心相互作用类型之间的共同部分会被重用。这些共同部分是:__

- __坐标检索__
- __计算标量距离__
- __将力的标量部分分散到两个中心__

__现在唯一剩下要做的就是调用实际内核来计算力。由于bond具有独特的类型，我们可以再次使用重载  
解析：__

__template < classT >  
auto bondKernel\(Tdr, const HarmonicBond&bond\)  
\{  
return harmonicScalarForce\(bond\.forceConstant\(\),bond\.equilDistance\(\),dr\);  
\}__

__然后调用实际内核,对简谐键形式最简单,看起来类似:__

__template < classT >  
std::tuple<T,T>harmonicScalarForce\(Tk,Tx0,Tx\)  
\{  
realdx =x\-x0;  
realdx2=dx\*dx;__

__realforce=\-k\*dx;__

__realepot=0\.5\*k\*dx2;__

__return std::make\_tuple\(force,epot\);__

__/\* That was 6 flops \*/  
\}__

__关于 __multithreading__ 的注意事项：多线程是在这里所述的顶级reduceListedForces之上处理的。对  
于并行执行，输入的ListedInteractions元组会被拆分成  
sphinxcodenThreads 个部分，并为每个线程设置一个 Buffer 对象。然后，每个线程都会调  
用一次 reduceListedForces，并将分配的 ListedInteractions 部分和 Buffer 作为参数。  
ListedInteractions拆分的存在时间与区域分解相关联。__

