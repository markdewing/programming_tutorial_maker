# Development of a mini C++ MPI3 wrapper
## First communication routine


The next step is to add a communication routine to the communicator class.

For simplicity, we will use broadcast.
For the C++ interface, we will add broadcast of a scalar value.

For the call to `MPI_Bcast` most of the parameters are straightforward  
 - the address of the value passed in, 
 - the count for a scalar is one
 - the datatype is more involved - will discuss below
 - the root value (optional value to the broadcast_value function)
 - the internal `MPI_Comm` value.

The biggest issue is the C++ type needs to be converted the MPI type enumeration.

Use a template class ('datatype') and specializations for each C++ type
contain an operator that converts to `MPI_Datatype`.
(There are other ways of representing this in the class - setting up
  a static 'value' set to the MPI data type)

For this mini mpi3, conversion for int and double is implemented.
For a more extensive list, a macro is used.

### Source
step3/mini_mpi3.hpp
```

#ifndef MINI_MPI3_HPP
#define MINI_MPI3_HPP

#include <stdexcept>

#include <mpi.h>

// Convert C++ type to MPI type enumeration
// int -> MPI_INT
// double -> MPI_DOUBLE
template <class T> class datatype;

template <> struct datatype<int> {
  operator MPI_Datatype() const{return MPI_INT;};
};

template <> struct datatype<double> {
  operator MPI_Datatype() const{return MPI_DOUBLE;};
};

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

  template<class T>
  void broadcast_value(T &t, int root = 0) {
    int count = 1;
    MPI_Datatype dt = datatype<T>{};
    MPI_Bcast(std::addressof(t), count, dt, root, impl_);
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
step3/test_main.cpp
```

#include <mini_mpi3.hpp>
#include <iostream>

int main()
{
  environment env;
  communicator world = env.world();

  int a = 1;
  if (world.rank() == 0) {a = 3;}
  world.broadcast_value(a);
  std::cout << "From rank " << world.rank()  << " a = " << a << std::endl;
  
  return 0;
}
```


### Run command
```

mpirun -np 4 ./a.out
```


### Run output 
```
From rank 0 a = 3
From rank 1 a = 3
From rank 2 a = 3
From rank 3 a = 3
```

Next: [Broadcast array](out_step4.md)

Prev: [Communicator](out_step2.md)
