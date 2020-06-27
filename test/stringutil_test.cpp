#include <gtest/gtest.h>
#define private public
#define protected public

#include "../../src/utility/stringutil.h"
using namespace ::testing;

class Global_stringutil_test : public ::testing::Test {
protected:
  virtual void SetUp() {
    // FIX ME!
  }
  virtual void TearDown() {
    // FIX ME!
  }
};

TEST(Global_stringutil_test, stob) {
  // FIX ME!
}

TEST(Global_stringutil_test, btos) {
  // FIX ME!
}

TEST(Global_stringutil_test, nextVersasBracket) {
  QString t = "{{a}}";
  ASSERT_EQ(nextVersasBracket(t, 0), 5);
  ASSERT_EQ(nextVersasBracket(t, 1), 4);
}

TEST(Global_stringutil_test, indent) {
  // FIX ME!
}

TEST(Global_stringutil_test, downIndent) {
  QString t = "{\n"
              "  {\n"
              "    a\n"
              "  }\n"
              "}\n";

  QString e1 = "{\n"
               "{\n"
               "  a\n"
               "}\n"
               "}\n";
  t = downIndent(t, 2);
  ASSERT_STREQ(t.toStdString().c_str(), e1.toStdString().c_str());

  QString e2 = "{\n"
               "{\n"
               "a\n"
               "}\n"
               "}\n";
  t = downIndent(t, 2);
  ASSERT_STREQ(t.toStdString().c_str(), e2.toStdString().c_str());
}

TEST(Global_stringutil_test, upIndent) {
  //  QString d = "{\n"
  //              "{\n"
  //              "a\n"
  //              "}\n"
  //              "}\n";

  //  QString dexp1 = "  {\n"
  //                  "  {\n"
  //                  "  a\n"
  //                  "  }\n"
  //                  "  }\n";
  //  d = upIndent(d, 2);
  //  ASSERT_STREQ(d.toStdString().c_str(), dexp1.toStdString().c_str());
}

TEST(Global_stringutil_test, stripBlacket) {
  QString t = "{\n"
              "  {\n"
              "    a\n"
              "  }\n"
              "}\n";

  QString e1 = "  {\n"
               "    a\n"
               "  }";
  QString t1 = stripBlacket(t, false);
  ASSERT_STREQ(t1.toStdString().c_str(), e1.toStdString().c_str());

  QString e2 = "    a";
  t1 = stripBlacket(t1, false);
  ASSERT_STREQ(t1.toStdString().c_str(), e2.toStdString().c_str());

  QString e3 = "{\n"
               "  a\n"
               "}";
  QString t2 = stripBlacket(t);
  ASSERT_STREQ(t2.toStdString().c_str(), e3.toStdString().c_str());

  QString e4 = "a";
  t2 = stripBlacket(t2);
  ASSERT_STREQ(t2.toStdString().c_str(), e4.toStdString().c_str());
}

TEST(Global_stringutil_test, removeContinuityBlank) {
  QString t = "    a   ";
  QString e = " a ";
  ASSERT_STREQ(removeContinuityBlank(t).toStdString().c_str(), e.toStdString().c_str());
}

TEST(Global_stringutil_test, systemIncludeCode) {
  QString t = systemIncludeCode("a");
  QString e = "#include <a>";
  ASSERT_STREQ(t.toStdString().c_str(), e.toStdString().c_str());
}

TEST(Global_stringutil_test, localIncludeCode) {
  QString t = localIncludeCode("a");
  QString e = "#include \"a\"";
  ASSERT_STREQ(t.toStdString().c_str(), e.toStdString().c_str());
}

TEST(Global_stringutil_test, defineCode) {
  QString t = defineCode("a", "b");
  QString e = "#define a b";
  ASSERT_STREQ(t.toStdString().c_str(), e.toStdString().c_str());
}

TEST(Global_stringutil_test, usingNamespaceCode) {
  QString t = usingNamespaceCode("a");
  QString e = "using namespace a;";
  ASSERT_STREQ(t.toStdString().c_str(), e.toStdString().c_str());
}

TEST(Global_stringutil_test, removeLastReturnDuplicate) {
  // FIX ME!
}
