
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
