#include <gtest/gtest.h>
#define private public
#define protected public

#include "../../src/utility/stringutil.h"
using namespace ::testing;

class stringutil_test : public ::testing::Test {
protected:
  virtual void SetUp() {
    // FIX ME!
  }
  virtual void TearDown() {
    // FIX ME!
  }
};

TEST_F(stringutil_test, stob) {
  // FIX ME!
}

TEST_F(stringutil_test, btos) {
  // FIX ME!
}

TEST_F(stringutil_test, nextVersasBracket) {
  QString t = "{{a}}";
  ASSERT_EQ(nextVersasBracket(t, 0), 5);
  ASSERT_EQ(nextVersasBracket(t, 1), 4);
  if(aaa){
    testtest
  }
}

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