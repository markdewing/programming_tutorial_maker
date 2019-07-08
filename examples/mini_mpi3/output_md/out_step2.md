# Development of a mini C++ MPI3 wrapper
## Communicator


Add a communicator class.  For now it contains a rank function to get the MPI rank.
Eventually it will contain most of the communication functions.

The raw `MPI_Comm` value is stored internally to the class.

Add a method to the environment to get a world communicator object.
(Todo: explain the use of static get_world_instance.)



### Source
step2/mini_mpi3.hpp
```

#ifndef MINI_MPI3_HPP
#define MINI_MPI3_HPP

#include <stdexcept>

#include <mpi.h>

class communicator
{
public:
  communicator(MPI_Comm impl) noexcept : impl_(impl) {}

  int rank() const {
    int rank = -1;
    int s = MPI_Comm_rank(impl_, &rank);
    if (s != MPI_SUCCESS) throw std::runtime_error("MPI_Comm_rank failed");
    return rank;
  }

private:
  MPI_Comm impl_;
};



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

  static inline communicator& get_world_instance()
  {
    static communicator instance{MPI_COMM_WORLD};
    return instance;
  }

  communicator world() const {
    communicator ret{get_world_instance()};
    return ret;
  }

};



#endif /* MINI_MPI3_HPP */
```

### Test code
step2/test_main.cpp
```

#include <mini_mpi3.hpp>
#include <iostream>


int main()
{
  environment env;
  communicator world = env.world();
  std::cout << "Hello from " << world.rank() << std::endl;
  return 0;
}
```


### Run command
```

mpirun -np 4 ./a.out
```


### Run output 
```
Hello from 2
Hello from 0
Hello from Hello from 3
1
```

Next: [First communication routine](out_step3.md)

Prev: [Initialization](out_step1.md)
