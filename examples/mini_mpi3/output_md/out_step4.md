# Development of a mini C++ MPI3 wrapper
## Broadcast array


The next improvement is to broadcast an array type with a start iterator and a length.
And make it work with a variety of array types (raw C++ arrays, STL containers)

Here the issue is obtaining the address corresponding to the start iterator.
We are assuming the container storage is contiguous.

One solution is to declare a templated `get_pointer` function
that is overloaded on different types - C++ pointer, STL iterator, etc.

### Source
step4/mini_mpi3.hpp
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


// Get address for different kinds of iterators
template <class T> auto get_pointer(T *t) { return t; }

template <class It> auto get_pointer(It it) { return it.base(); }




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

  template <class It, typename Size>
  void broadcast_n(It first, Size count, int root = 0) {
    MPI_Datatype dt = datatype<typename std::iterator_traits<It>::value_type>{};
    MPI_Bcast(get_pointer(first), count, dt, root, impl_);
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
step4/test_main.cpp
```

#include <mini_mpi3.hpp>
#include <iostream>
#include <vector>

int main()
{
  environment env;
  communicator world = env.world();

  // Broadcast_n with raw C++ array
  double va[3]; 
  if (world.rank() == 0) {va[0] = 1.1;}
  world.broadcast_n(va, 3);
  std::cout << "From rank " << world.rank()  << " va[0] = " << va[0] << std::endl;

  // Broadcast_n with std::vector
  std::vector<double> vv{1.0, 2.0, 3.0};
  if (world.rank() == 0) {vv[0] = 4.0;}
  world.broadcast_n(vv.begin(), vv.size());
  std::cout << "From rank " << world.rank()  << " vv[0] = " << vv[0] << std::endl;
  
  return 0;
}
```


### Run command
```

mpirun -np 4 ./a.out
```


### Run output 
```
From rank 0 va[0] = 1.1
From rank 0 vv[0] = 4
From rank 1 va[0] = 1.1
From rank 1 vv[0] = 4
From rank 2 va[0] = 1.1
From rank 2 vv[0] = 4
From rank 3 va[0] = 1.1
From rank 3 vv[0] = 4
```


Prev: [First communication routine](out_step3.md)
