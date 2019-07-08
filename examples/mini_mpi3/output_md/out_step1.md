# Development of a mini C++ MPI3 wrapper
## Initialization


The first step is to call `MPI_Init` and `MPI_Finalize`.

Create an `environment` class that performs these functions for the lifetime of the
object.

For simplicity, MPI_Init is called with null pointers.


### Source
step1/mini_mpi3.hpp
```

#ifndef MINI_MPI3_HPP
#define MINI_MPI3_HPP

#include <stdexcept>

#include <mpi.h>


inline void finalize()
{
  int s = MPI_Finalize();
  if (s != MPI_SUCCESS) throw std::runtime_error("cannot finalize MPI");

}

inline void initialize(){
  int s = MPI_Init(nullptr, nullptr);
  if (s != MPI_SUCCESS) throw std::runtime_error("cannot initialize MPI");
}


class environment
{
public:
  environment() { initialize(); }
  ~environment() { finalize(); }
};



#endif /* MINI_MPI3_HPP */
```

### Test code
step1/test_main.cpp
```

#include <mini_mpi3.hpp>
#include <iostream>


int main()
{
  environment env;
  std::cout << "Hello" << std::endl;
  return 0;
}
```


### Run command
```

mpirun -np 4 ./a.out
```


### Run output 
```
Hello
Hello
Hello
Hello
```

Next: [Communicator](out_step2.md)
