#include "toptobottomtreelayoutproxy.h"
#include "utility/systemconfig.h"
#include "viewmodel/graphicsitem/connection.h"
#include "viewmodel/graphicsitem/node.h"
#include <QDebug>
#include <QRectF>

const QPointF OFFSET(0, 10);
const QPointF CUBIC_POINT(0, 10);

const QString TopToBottomTreeLayoutProxy::NAME = "Top To Bottom";

TopToBottomTreeLayoutProxy::TopToBottomTreeLayoutProxy() : AbstractLayoutProxy() {
}

TopToBottomTreeLayoutProxy::~TopToBottomTreeLayoutProxy() {
}

void TopToBottomTreeLayoutProxy::layout(Node* rootNode) {
  if (rootNode) {
    layoutChild(rootNode);
  }
}

QString TopToBottomTreeLayoutProxy::name() const {
  return NAME;
}

qreal TopToBottomTreeLayoutProxy::layoutChild(const Node* node) {
  const QRectF br = node->boundingRect();
  if (!node->hasChild()) {
    return br.width();
  }
  const qreal y = br.bottom() + systemConfig(SystemConfig::topToBottomTreeLayoutNodeYSpace).toReal();
  const qreal childWidth = childrenWidth(node);
  qreal x = br.center().x() - childWidth / 2;
  foreach (Node* childNode, node->childNodes()) {
    const qreal th = layoutChild(childNode);
    childNode->setPos(x + th / 2 - childNode->boundingRect().center().x(), y);
    x += th + systemConfig(SystemConfig::topToBottomTreeLayoutNodeXSpace).toReal();
    drawConnection(node, childNode);
  }
  return qMax(childWidth, br.bottom());
}

qreal TopToBottomTreeLayoutProxy::treeWidth(const Node* node) {
  return qMax(childrenWidth(node), node->boundingRect().width());
}

qreal TopToBottomTreeLayoutProxy::childrenWidth(const Node* node) {
  if (!node->hasChild()) {
    return 0;
  }
  qreal topToBottomLayoutNodeXSpace = systemConfig(SystemConfig::topToBottomTreeLayoutNodeXSpace).toReal();
  qreal width = -topToBottomLayoutNodeXSpace;
  foreach (Node* childNode, node->childNodes()) {
    width += treeWidth(childNode);
    width += topToBottomLayoutNodeXSpace;
  }
  return width;
}

void TopToBottomTreeLayoutProxy::drawConnection(const Node* parentNode, const Node* childNode) {
  QPointF parentToChild = parentNode->scenePos() - childNode->scenePos();
  QPointF parentPos = parentToChild + parentNode->bottomCenter() + OFFSET;
  QPointF childPos = childNode->topCenter() - OFFSET;
  childNode->connection()->draw(parentPos, childPos, CUBIC_POINT);
}
