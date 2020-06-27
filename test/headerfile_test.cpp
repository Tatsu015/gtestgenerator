#include <gtest/gtest.h>
#define private public
#define protected public

using namespace ::testing;

class HeaderFile_test : public ::testing::Test {
protected:
  virtual void SetUp() {
    // FIX ME!
  }
  virtual void TearDown() {
    // FIX ME!
  }
};

TEST(HeaderFile_test, HeaderFile) {
  // FIX ME!
}

TEST(HeaderFile_test, parse) {
  // FIX ME!
}

TEST(HeaderFile_test, removeCComment) {
  // FIX ME!
}

TEST(HeaderFile_test, removeCppComment) {
  // FIX ME!
}

TEST(HeaderFile_test, removeForwardDeclaration) {
  // FIX ME!
}

TEST(HeaderFile_test, parseFunctions) {
  // FIX ME!
}

TEST(HeaderFile_test, parseFunction) {
  // FIX ME!
}
